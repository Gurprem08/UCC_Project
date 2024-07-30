import mysql.connector
import pandas as pd
from flask import Flask, jsonify, request, send_file, make_response
import pypyodbc  as odbc 
import json
from flask_socketio import SocketIO, emit
from io import StringIO


socketio = SocketIO()

connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:guru0008.database.windows.net,1433;Database=Water_quality;Uid=guru0008;Pwd={Guru@12345678};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30';


# Function to connect to MySQL database
def create_db_connection():
    try:
        connection = odbc.connect(connection_string)


        if connection:
            print("Successfully connected to the database")
            return connection
    except Exception as e:
        print(f"Error: {e}")
        return None

# Function to insert data into the MySQL database
def insert_data_to_db(df,socketio):
    connection = create_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                IF NOT EXISTS (SELECT * FROM sys.tables WHERE name='water_quality_predictions')
                BEGIN
                    CREATE TABLE water_quality_predictions(        
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    pH FLOAT, 
                    EC FLOAT, 
                    TDS FLOAT, 
                    Temperature FLOAT,
                    p_CO3 FLOAT, 
                    p_CL FLOAT, 
                    p_SO4 FLOAT, 
                    p_TH FLOAT, 
                    p_CA FLOAT, 
                    p_MG FLOAT, 
                    p_NA FLOAT,
                    WQI FLOAT,
                    State VARCHAR(255),
                    Date DATE
                );
            END
            """)
            print("Table created successfully or already exists")

            for _, row in df.iterrows():
                # Convert each value in the row to a native Python float type

                values = tuple(float(f"{x:.3f}") if not isinstance(x, str) else x for x in row)

                
                cursor.execute(
                    """
                    INSERT INTO water_quality_predictions 
                    (pH, EC, TDS, Temperature, p_CO3, p_CL, p_SO4, p_TH, p_CA, p_MG, p_NA, WQI, State, Date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    values
                )
            connection.commit()
            print("Data inserted into the database successfully!")
             # Send notification to the client side
            # socketio.emit('Important_message', {'message': 'secret'})

        except Exception as e:
            print(f"Error while inserting data: {e}")
        finally:
            cursor.close()
            connection.close()

def get_CSV_values():
    connection = create_db_connection()
    if connection:
        try:
            query = "SELECT * FROM water_quality_predictions"
            df1 = pd.read_sql(query, connection)
            csv_buffer = StringIO()
            df1.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)
            connection.close()

            response = make_response(csv_buffer.getvalue())
            response.headers['Content-Disposition'] = 'attachment; filename=water_quality_predictions.csv'
            response.headers['Content-Type'] = 'text/csv'
            return response
        
        except Exception as e:
            print(f'Error: {e}')
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500