import pandas as pd
import pyodbc
from sqlalchemy import create_engine

def excel_to_sql(excel_file, table_name, user, password, host, port, database):
    # Read the CSV file into a Pandas DataFrame
    df = pd.read_excel(excel_file,sheet_name='Sheet1')
    # print(df)
    # Create the database URL for SQLAlchemy
    # database_url = f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    # connection_string = f'mssql+pyodbc://nirbhay:admin@1234@tcp:dq-sql-server.database.windows.net,1433/exception_database?driver=ODBC+Driver+17+for+SQL+Server'
    database_url = '{ODBC Driver 17 for SQL Server};Server=tcp:dq-sql-server.database.windows.net,1433;Database=exception_database;Uid=nirbhay;Pwd=admin@1234;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'
    
    # Create an SQLAlchemy engine
    engine = create_engine(database_url)
    try:
        # Connect to the database and return the connection engine
        connection = engine.connect()
        print("Connected to Azure SQL Database successfully!")
        return engine
    except Exception as e:
        print("Error connecting to Azure SQL Database:", str(e))
        return None

    # Write the DataFrame to the SQL database
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    
    print(f"Data from {excel_file} has been stored in the '{table_name}' table of the database.")

# Example usage:
excel_file = 'C:\\Users\\Sahil Agarwal\\Desktop\\Innovation Fair\\250k_AS_dataset.xlsx'  # Replace with your CSV file path
table_name = 'new_dataset'  # Replace with your desired table name
user = 'root'
password = 'admin'
host = 'localhost'
port = 3306
database = 'exception_database'

excel_to_sql(excel_file, table_name, user, password, host, port, database)

import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/database_name"

# Excel file path
EXCEL_FILE_PATH = "example.xlsx"
TABLE_NAME = "your_table_name"

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

def insert_data_in_chunks(file_path, table_name, engine, chunk_size=1000):
    """
    Inserts data from an Excel file into a MySQL database in chunks.

    Args:
        file_path (str): Path to the Excel file.
        table_name (str): Name of the MySQL table to insert data.
        engine: SQLAlchemy engine object.
        chunk_size (int): Number of rows to process in each chunk.
    """
    print("Reading Excel file...")
    total_rows = sum(1 for _ in pd.read_excel(file_path, sheet_name=0)) - 1  # Exclude header row
    print(f"Total rows to insert: {total_rows}")

    # Read Excel in chunks
    reader = pd.read_excel(file_path, sheet_name=0, chunksize=chunk_size)
    chunk_number = 0

    for chunk in reader:
        chunk_number += 1
        print(f"Inserting chunk {chunk_number} containing {len(chunk)} rows...")
        try:
            chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)
            print(f"Successfully inserted chunk {chunk_number}.")
        except Exception as e:
            print(f"Error inserting chunk {chunk_number}: {e}")
            continue

    print("Data insertion completed.")

# Call the function
insert_data_in_chunks(EXCEL_FILE_PATH, TABLE_NAME, engine)
