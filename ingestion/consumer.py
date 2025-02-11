import json
import pika
import pandas as pd
from sqlalchemy import create_engine
from collections import defaultdict

# ---------------------------
# Database config
# ---------------------------
DB_URI = "postgresql://myuser:mypassword@localhost:5432/mydatabase"
engine = create_engine(DB_URI)

# ---------------------------
# RabbitMQ config
# ---------------------------
RABBIT_HOST = "localhost"
QUEUE_NAME = "file_data_queue"
BATCH_SIZE = 10  # how many messages to accumulate per (dataset, part)

connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
channel = connection.channel()
channel.queue_declare(queue=QUEUE_NAME)

# We will keep a dictionary of buffers, keyed by (dataset, part).
# Each buffer holds a list of row dicts ("rows") and their delivery_tags ("tags").
buffers = defaultdict(lambda: {"rows": [], "tags": []})

def get_table_name(dataset, part):
    """
    Returns the table name for the given dataset and part.
    E.g. FD001_train, FD001_test, FD001_rul, FD002_train, etc.
    """
    return f"{dataset}_{part}"

def flush_buffer(dataset, part):
    """
    Writes the buffered rows for (dataset, part) to the DB in one batch,
    then ACKs all messages up to the highest delivery_tag.
    """
    key = (dataset, part)
    row_buffer = buffers[key]["rows"]
    tag_buffer = buffers[key]["tags"]

    if not row_buffer:
        return

    # Convert list of row dicts to a DataFrame
    df = pd.DataFrame(row_buffer)

    # Decide on the target table
    table_name = get_table_name(dataset, part)

    # Insert into the DB
    df.to_sql(name=table_name,
              con=engine,
              if_exists='append',
              index=False)

    # Acknowledge all messages (bulk ACK)
    last_tag = max(tag_buffer)
    channel.basic_ack(delivery_tag=last_tag, multiple=True)

    # Clear the buffers for this key
    buffers[key]["rows"].clear()
    buffers[key]["tags"].clear()

    print(f"Flushed {len(df)} rows to table '{table_name}'. ACKed up to delivery_tag={last_tag}.")

def flush_all_buffers():
    """
    Flushes all buffers for all (dataset, part) keys, useful on shutdown.
    """
    for (ds, part), _ in buffers.items():
        flush_buffer(ds, part)

def on_message(ch, method, properties, body):
    """
    Callback function for incoming messages.
    Each message is expected to have:
      {
        "dataset": "FD001",
        "part": "train"|"test"|"rul",
        "row": { ... row data ... }
      }
    We accumulate them in the buffers dict under the key (dataset, part).
    When the buffer hits BATCH_SIZE, we flush it to the DB.
    """
    message_dict = json.loads(body.decode('utf-8'))
    dataset = message_dict["dataset"]
    part = message_dict["part"]
    row_data = message_dict["row"]

    # Accumulate
    buffers[(dataset, part)]["rows"].append(row_data)
    buffers[(dataset, part)]["tags"].append(method.delivery_tag)

    # Check if we've hit BATCH_SIZE for this (dataset, part)
    if len(buffers[(dataset, part)]["rows"]) >= BATCH_SIZE:
        flush_buffer(dataset, part)

# Use manual acknowledgments
channel.basic_qos(prefetch_count=BATCH_SIZE)
channel.basic_consume(queue=QUEUE_NAME,
                      on_message_callback=on_message,
                      auto_ack=False)

print(" [*] Waiting for messages (across all FD datasets). To exit press CTRL+C.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    print("Stopping consumer...")

# On exit, flush any leftover rows
flush_all_buffers()

channel.stop_consuming()
connection.close()
