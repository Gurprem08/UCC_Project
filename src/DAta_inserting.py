import csv
import pypyodbc  as odbc 
import pandas as pd


connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:guru0008.database.windows.net,1433;Database=Water_quality;Uid=guru0008;Pwd={Guru@12345678};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30';
df = ('push.csv')


# Function to connect to MySQL database
def create_db_connection():
    try:
        connection = odbc.connect(connection_string)
        # connection = mysql.connector.connect(
        # user= 'root',                # Replace with your actual MySQL username
        # password= 'Guru@12345678',   # Replace with your actual MySQL password
        # host= '127.0.0.1',           # Host where your MySQL server is running
        # port= 3306,                  # Port number for your MySQL server
        # database= 'Streamlit_DB'     # Replace with your actual database name
        # )

        if connection:
            print("Successfully connected to the database")
            return connection
    except Exception as e:
        print(f"Error: {e}")
        return None


# Establish connection
def insert_data_to_db():
    connection = create_db_connection()
    if connection:
        
        cursor = connection.cursor()
        

# SQL insert statement
        sql_insert = """
INSERT INTO Tab_data (
    State, District, Block, Location, Latitude, Longitude, Year, pH, EC, CO3, Cl, SO4, TH, Ca, Mg, Na, TDS, Temperature,
    St_Temp, St_pH, St_EC, St_CO3, St_CL, St_SO4, St_TH, St_CA, St_Mg, St_Na, St_TDS, WQI
) 
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

        try:
    # Open and read CSV file
            with open(df, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.reader(csvfile)
                next(reader)  # Skip header row if exists

        # Iterate over rows and execute insert
                for row in reader:
                    
                    cursor.execute(sql_insert, row)
                    connection.commit()
                    print(f'Inserted row: {row}')
        

            print('Data insertion process completed')
        except Exception as e:
            print(f'Error reading CSV file: {str(e)}')
        finally:
            cursor.close()
            connection.close()
            print('Connection closed')


if __name__ == "__main__":
     insert_data_to_db()