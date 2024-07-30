from flask import Flask, jsonify, request, send_file, make_response
from flask_cors import CORS 
import json
import numpy as np
from ml_model import predict
import pandas as pd
from water_quality import calculate_wqi
from Database_connec import insert_data_to_db
from Database_connec import get_CSV_values
from io import StringIO
from flask_socketio import SocketIO




app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins='*')
CORS(app)



@app.route('/api/default_csv', methods=['GET'])
def get_defaut_CSV():
    # Create a DataFrame with the required columns
    default_data = {
    'State': [],
    'Date(dd-mm-yyyy)': [],
    'pH': [],
    'EC(uS/cm)': [],
    'TDS(mg/L)': [],
    'Temperature(C)': [],

}

    df = pd.DataFrame(default_data)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    response = make_response(csv_buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=default_csv.csv'
    response.headers['Content-Type'] = 'text/csv'

    return(response)

@app.route ('/api/CSV', methods = ["GET"])
def get_CSV():
    return(get_CSV_values())


@app.route('/api/predict', methods=['POST'])
def post_data():
    try:
        input_data = request.json
                # Extract values from the received JSON object
        pH = input_data.get('ph')
        EC = input_data.get('ec')
        TDS = input_data.get('tds')
        Temperature = input_data.get('temperature')
        State = input_data.get('selectedState')
        Date = input_data.get('selectedDate')
        

                # Convert values to the appropriate data types
        pH = float(pH) if pH else None
        EC = float(EC) if EC else None
        TDS = float(TDS) if TDS else None
        Temperature = float(Temperature) if Temperature else None

        # Call your machine learning function to get predictions
        parameters = [pH, EC, TDS, Temperature]

        predictions = predict(parameters)
         # Convert numpy arrays to regular Python lists or floats
        predicted_data = {key:  round(float(value), 4) if isinstance(value, np.ndarray) else float(value) for key, value in predictions.items()}


        #Creating Dataframes

        # Extract predicted values and construct DataFrame
        df= pd.DataFrame({
        'pH': [pH],
        'EC': [EC],
        'TDS': [TDS],
        'Temperature': [Temperature],       
        'p_CO3':predicted_data['CO3'],
        'p_CL': predicted_data['Cl'],
        'p_SO4':predicted_data['SO4'],
        'p_TH': predicted_data['TH'],
        'p_CA': predicted_data['Ca'],
        'p_MG': predicted_data['Mg'],
        'p_NA': predicted_data['Na']
})

    # Calculate WAWQI
        standard_values = {
    'p_CO3': 250,
    'p_CL': 250,
    'p_SO4': 250,
    'p_TH': 500,
    'p_CA': 75,
    'p_MG': 30,
    'p_NA': 200,
    'pH': 8.5,
    'TDS': 500
}

        ideal_values = {
    'p_CO3': 0,
    'p_CL': 0,
    'p_SO4': 0,
    'p_TH': 0,
    'p_CA': 0,
    'p_MG': 0,
    'p_NA': 0,
    'pH': 7,
    'TDS': 0
}

        weights = {
    'p_CO3': 1,
    'p_CL': 1,
    'p_SO4': 1,
    'p_TH': 1,
    'p_CA': 1,
    'p_MG': 1,
    'p_NA': 1,
    'pH': 1,
    'TDS': 1
}

        WAWQI = calculate_wqi(df.to_dict('records')[0], standard_values, ideal_values, weights)
        WAWQI = round(float(WAWQI), 4)
        df["WQI"] = WAWQI
        df["State"] = str(State)
        df["Date"] = Date
        

 
        insert_data_to_db(df,socketio)

        processed_data = {
    'received': input_data,
    'predictions': predicted_data,
    'WAWQI': WAWQI,
    'message': 'Data received and processed'
}
        return jsonify(processed_data),200
    except Exception as e:
        print(f'Error is  {e}')
        return jsonify({"error": str(e)}), 500

    

@app.route('/api/predict_with_csv', methods = ["POST"])
def predict_with_csv():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if file:
            data = pd.read_csv(file)
            results = []
            for _, row in data.iterrows():
                pH = row.get('pH')
                EC = row.get('EC')
                TDS = row.get('TDS')
                Temperature = row.get('Temperature')
                State = row.get('State')
                Date = row.get('Date')
                
                # Convert values to the appropriate data types
                pH = float(pH) if pH else None
                EC = float(EC) if EC else None
                TDS = float(TDS) if TDS else None
                Temperature = float(Temperature) if Temperature else None
                
                # Call your machine learning function to get predictions
                parameters = [pH, EC, TDS, Temperature]
                predictions = predict(parameters)

                # Convert numpy arrays to regular Python lists or floats
                predicted_data = {key: round(float(value), 4) if isinstance(value, np.ndarray) else float(value) for key, value in predictions.items()}

                # Construct DataFrame for each row
                df_row = pd.DataFrame({
                    'pH': [pH],
                    'EC': [EC],
                    'TDS': [TDS],
                    'Temperature': [Temperature],
                    'p_CO3': predicted_data['CO3'],
                    'p_CL': predicted_data['Cl'],
                    'p_SO4': predicted_data['SO4'],
                    'p_TH': predicted_data['TH'],
                    'p_CA': predicted_data['Ca'],
                    'p_MG': predicted_data['Mg'],
                    'p_NA': predicted_data['Na']
                })

                # Calculate WAWQI
                standard_values = {
                    'p_CO3': 250,
                    'p_CL': 250,
                    'p_SO4': 250,
                    'p_TH': 500,
                    'p_CA': 75,
                    'p_MG': 30,
                    'p_NA': 200,
                    'pH': 8.5,
                    'TDS': 500
                }

                ideal_values = {
                    'p_CO3': 0,
                    'p_CL': 0,
                    'p_SO4': 0,
                    'p_TH': 0,
                    'p_CA': 0,
                    'p_MG': 0,
                    'p_NA': 0,
                    'pH': 7,
                    'TDS': 0
                }

                weights = {
                    'p_CO3': 1,
                    'p_CL': 1,
                    'p_SO4': 1,
                    'p_TH': 1,
                    'p_CA': 1,
                    'p_MG': 1,
                    'p_NA': 1,
                    'pH': 1,
                    'TDS': 1
                }

                WAWQI = calculate_wqi(df_row.to_dict('records')[0], standard_values, ideal_values, weights)
                WAWQI = round(float(WAWQI), 4)
                df_row["WQI"] = WAWQI
                df_row["State"] = str(State)
                df_row["Date"] = Date

                
                results.append(df_row)
             
            # Combine all results into a single DataFrame
            final_df = pd.concat(results, ignore_index=True)
            df = convert_date_format(final_df)
            insert_data_to_db(df,socketio)

            return jsonify({"message": "File processed successfully", "data": df.to_json(orient='records')})

    except Exception as e:
        print(f'Error is {e}')
        return jsonify({"error": str(e)}), 500
    
def convert_date_format(df):
    # Assuming 'df' is your DataFrame with a 'Date' column in 'dd-mm-yyyy' format
    # Convert 'Date' column to datetime format and change its format
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y').dt.strftime('%Y-%m-%d')
    
    return df
if __name__ == '__main__':
    socketio.run(app, debug=True)

    