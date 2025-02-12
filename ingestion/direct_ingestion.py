import os
import pandas as pd
from sqlalchemy import create_engine

# ------------------------------------------------------------------------------
# 1) Configure your database connection here
# Replace this with the appropriate URI for your DB
# Docker command:
    # docker run -d `
    #   --name my-postgres `
    #   -p 5432:5432 `
    #   -e POSTGRES_USER=myuser `
    #   -e POSTGRES_PASSWORD=mypassword `
    #   -e POSTGRES_DB=mydatabase `
    #   postgres:latest
# ------------------------------------------------------------------------------
DB_URI = "postgresql://myuser:mypassword@localhost:5432/mydatabase"



# Create a global SQLAlchemy engine
engine = create_engine(DB_URI)

# ------------------------------------------------------------------------------
# 2) Define all column names for the 26 columns in the train/test files
#    Format:
#      1) unit number
#      2) time (in cycles)
#      3) op setting 1
#      4) op setting 2
#      5) op setting 3
#      6) sensor measurement 1
#      ...
#     26) sensor measurement 26
# ------------------------------------------------------------------------------
COLUMN_NAMES = [
    "engine_id",  # col 1: unit number
    "cycle",  # col 2: time in cycles
    "op_setting_1",  # col 3
    "op_setting_2",  # col 4
    "op_setting_3",  # col 5
    "sensor_1",  # col 6
    "sensor_2",  # col 7
    "sensor_3",  # col 8
    "sensor_4",  # col 9
    "sensor_5",  # col 10
    "sensor_6",  # col 11
    "sensor_7",  # col 12
    "sensor_8",  # col 13
    "sensor_9",  # col 14
    "sensor_10",  # col 15
    "sensor_11",  # col 16
    "sensor_12",  # col 17
    "sensor_13",  # col 18
    "sensor_14",  # col 19
    "sensor_15",  # col 20
    "sensor_16",  # col 21
    "sensor_17",  # col 22
    "sensor_18",  # col 23
    "sensor_19",  # col 24
    "sensor_20",  # col 25
    "sensor_21"  # col 26
]


# ------------------------------------------------------------------------------
# 3) Function to ingest a single FD dataset
#    This function:
#      - Reads train, test, and RUL files
#      - Creates "engine_data" DataFrame with a column "source" = 'train'/'test'
#      - Creates "rul_data" DataFrame with columns [dataset_name, engine_id, rul]
#      - Writes them to the DB
# ------------------------------------------------------------------------------
def ingest_fd_data(dataset_name, folder_path):
    """
    dataset_name: str, e.g. 'FD001'
    folder_path: path to the folder that contains
                 train_FDXXX.txt, test_FDXXX.txt, RUL_FDXXX.txt
    """
    # 3.1) Paths to each file
    train_file = os.path.join("data/raw", f"train_{dataset_name}.txt")
    test_file = os.path.join("data/raw", f"test_{dataset_name}.txt")
    rul_file = os.path.join("data/raw", f"RUL_{dataset_name}.txt")



    # 3.2) Read the TRAIN file
    train_df = pd.read_csv(
        train_file,
        sep=r"\s+",  # space-delimited
        header=None,  # no header
        names=COLUMN_NAMES
    )
    train_df["dataset_name"] = dataset_name
    train_df["source"] = "train"

    # 3.3) Read the TEST file
    test_df = pd.read_csv(
        test_file,
        sep=r"\s+",
        header=None,
        names=COLUMN_NAMES
    )
    test_df["dataset_name"] = dataset_name
    test_df["source"] = "test"

    # 3.4) Read the RUL file
    #      RUL_FDXXX.txt typically has 1 RUL value per test engine (N lines).
    #      We'll assume each line corresponds to engine_id = 1, 2, 3, ... in order.
    rul_series = pd.read_csv(
        rul_file,
        sep=r"\s+",
        header=None,
        names=["rul"]
    )["rul"]

    # Construct a DataFrame with engine_id, RUL
    # The engine IDs in the test set for FD001, for example, go from 1..100
    # We can confirm from the test set's "engine_id" how many unique engines we have.
    unique_engines_test = sorted(test_df["engine_id"].unique())
    # The length of rul_series should match the number of unique engines in test set.

    rul_df = pd.DataFrame({
        "engine_id": unique_engines_test,
        "rul": rul_series
    })
    rul_df["dataset_name"] = dataset_name

    # 3.5) Merge train and test data
    combined_sensor_data = pd.concat([train_df, test_df], ignore_index=True)

    # 3.6) Write dataframes to the DB
    #      Table 1: "engine_data"
    #      Table 2: "rul_data"

    # Write or append to engine_data table
    combined_sensor_data.to_sql(
        name= dataset_name + "_engine_data",
        con=engine,
        if_exists="append",  # or 'replace' if you want to overwrite
        index=False
    )

    # Write or append to rul_data table
    rul_df.to_sql(
        name=dataset_name + "_rul_data",
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Dataset {dataset_name} ingested: train={train_df.shape}, test={test_df.shape}, RUL={rul_df.shape}")


# ------------------------------------------------------------------------------
# 4) Master routine to ingest FD001, FD002, FD003, FD004
# ------------------------------------------------------------------------------
def main():
    base_folder = "../data/raw"  # Adjust to your folder

    # For each FDXXX, call the ingestion function
    for ds in ["FD001","FD002", "FD003", "FD004"]:
        ingest_fd_data(ds, base_folder)


if __name__ == "__main__":
    main()
