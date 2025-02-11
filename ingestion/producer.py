import pika
import os
import pandas as pd
import json

# RabbitMQ connection details
RABBIT_HOST = 'localhost'
QUEUE_NAME = 'file_data_queue'

# List the 4 FD datasets
FD_DATASETS = ["FD001", "FD002", "FD003", "FD004"]

def produce_all_data(base_folder):
    """
    Reads train, test, and RUL files for each FD dataset,
    converts rows to JSON messages, and publishes them to RabbitMQ.
    The JSON contains:
      {
        "dataset": "FD001",
        "part": "train" | "test" | "rul",
        "row": { ... columns ... }
      }
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBIT_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    for ds in FD_DATASETS:
        # Build file paths
        train_file = os.path.join(base_folder, f"train_{ds}.txt")
        test_file = os.path.join(base_folder, f"test_{ds}.txt")
        rul_file  = os.path.join(base_folder, f"RUL_{ds}.txt")

        # 1) Publish TRAIN data
        if os.path.isfile(train_file):
            train_df = pd.read_csv(train_file, sep=r"\s+", header=None)
            for _, row in train_df.iterrows():
                message_dict = {
                    "dataset": ds,
                    "part": "train",
                    "row": row.to_dict()  # numeric indices as keys
                }
                channel.basic_publish(
                    exchange='',
                    routing_key=QUEUE_NAME,
                    body=json.dumps(message_dict).encode('utf-8')
                )
            print(f"Sent {len(train_df)} 'train' rows for {ds} to RabbitMQ.")

        # 2) Publish TEST data
        if os.path.isfile(test_file):
            test_df = pd.read_csv(test_file, sep=r"\s+", header=None)
            for _, row in test_df.iterrows():
                message_dict = {
                    "dataset": ds,
                    "part": "test",
                    "row": row.to_dict()
                }
                channel.basic_publish(
                    exchange='',
                    routing_key=QUEUE_NAME,
                    body=json.dumps(message_dict).encode('utf-8')
                )
            print(f"Sent {len(test_df)} 'test' rows for {ds} to RabbitMQ.")

        # 3) Publish RUL data
        #    Usually each line has one RUL value for engine_id 1..N in order
        if os.path.isfile(rul_file):
            rul_series = pd.read_csv(rul_file, sep=r"\s+", header=None).iloc[:,0]
            # Build an engine_id range (assuming RUL file lines correspond to engine_id=1..N)
            for engine_id, rul_value in enumerate(rul_series, start=1):
                message_dict = {
                    "dataset": ds,
                    "part": "rul",
                    "row": {
                        "engine_id": engine_id,
                        "rul": rul_value
                    }
                }
                channel.basic_publish(
                    exchange='',
                    routing_key=QUEUE_NAME,
                    body=json.dumps(message_dict).encode('utf-8')
                )
            print(f"Sent {len(rul_series)} 'rul' rows for {ds} to RabbitMQ.")

    connection.close()
    print("All FD datasets have been published to RabbitMQ.")

if __name__ == "__main__":
    # Adjust base_folder to point to where your FD files live
    base_folder = "../data/raw"
    produce_all_data(base_folder)
