import pandas as pd
from sqlalchemy import create_engine


def insert_data_in_chunks(file_path, table_name, engine, chunk_size=10000):
    """
    Inserts data from an Excel file into a MySQL database in chunks.

    Args:
        file_path (str): Path to the Excel file.
        table_name (str): Name of the MySQL table to insert data.
        engine: SQLAlchemy engine object.
        chunk_size (int): Number of rows to process in each chunk.
    """
    print("Reading Excel file...")
    total_rows = pd.read_excel(file_path, sheet_name='Sheet1').shape[0]  # Exclude header row
    print(f"Total rows to insert: {total_rows}")

    # Read Excel in chunks
    # reader = pd.read_excel(file_path, sheet_name=0, chunksize=chunk_size)
    chunk_number = 0

    for start_row in range(0, total_rows, chunk_size):
        chunk_number += 1
        print(f"Inserting chunk {chunk_number} containing {start_row} to {start_row + chunk_size - 1} rows...")
        try:
            chunk = pd.read_excel(file_path,sheet_name='Sheet1',skiprows=range(1,start_row+1),nrows=chunk_size)
            chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)
            print(f"Successfully inserted chunk {chunk_number}.")
        except Exception as e:
            print(f"Error inserting chunk {chunk_number}: {e}")
            continue

    print("Data insertion completed.")


# Database connection details
DATABASE_URL = "mysql+pymysql://root:admin@localhost:3306/exception_database2"

# Excel file path
EXCEL_FILE_PATH = "C:\\Users\\Sahil Agarwal\\Desktop\\Innovation Fair\\250k_AS_dataset.xlsx"
TABLE_NAME = "new_dq"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Call the function
insert_data_in_chunks(EXCEL_FILE_PATH, TABLE_NAME, engine)
