import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import chardet

# Function to create a connection to the MySQL database
def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host='',
            user='',
            passwd='',
            database=''
        )
        print("Connection to MySQL DB successful")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("The credentials you provided are not valid.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("The database does not exist.")
        else:
            print(err)
    return connection

# Function to execute a query
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except mysql.connector.Error as err:
        print(f"Error: '{err}'")

# Function to insert data into a table
def insert_data(connection, df, table_name):
    cursor = connection.cursor()
    for _, row in df.iterrows():
        sql = f"INSERT INTO {table_name} VALUES (" + ", ".join(["%s"] * len(row)) + ")"
        cursor.execute(sql, tuple(row))
    connection.commit()
    print(f"Data inserted successfully into {table_name}")

# Read CSV file into a DataFrame
csv_file_path = ''
with open(csv_file_path, 'rb') as f:
    encoding = chardet.detect(f.read())['encoding']
print(encoding)
df = pd.read_csv(csv_file_path, encoding=encoding)
df.fillna('', inplace=True)

# Database connection details
host = ""
user = ""
password = ""
database = ""

# Create a connection to the database
connection = create_connection(host, user, password, database)

# Define the table name and schema based on the CSV columns
table_name = "rabies_raw_data"
columns = ", ".join([f"{col} TEXT" for col in df.columns])

# Create the table query
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    {columns}
);
"""

# Execute the table creation query
execute_query(connection, create_table_query)

# Insert data into the table
insert_data(connection, df, table_name)

# Close the connection
if connection.is_connected():
    connection.close()
    print("MySQL connection is closed")