import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
data = pd.read_csv('f_dataset.csv')

# Basic parameters used as input
input_features = ['Temperature', 'EC', 'TDS', 'pH']

# Target parameters to predict
target_features = ['CO3', 'HCO3', 'Cl', 'SO4', 'NO3', 'TH', 'Ca', 'Mg', 'Na', 'K', 'F']

# Splitting data into input and target variables
X = data[input_features]
y = data[target_features]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Reshape input data to 3D for LSTM
X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))

# Define the LSTM model
def create_lstm_model(input_shape):
    model = tf.keras.Sequential([
        tf.keras.layers.LSTM(50, input_shape=input_shape),
        tf.keras.layers.Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Dictionary to hold the models and their predictions
models = {}
predictions = {}
results = {}
r2_results = {}

# Train and evaluate a separate LSTM model for each target parameter
for target in target_features:
    print(f'Training model for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]
    
    # Define and create LSTM model
    model = create_lstm_model(input_shape=(X_train.shape[1], X_train.shape[2]))
    
    # Train the model
    model.fit(X_train, y_target_train, epochs=100, batch_size=16, verbose=0)
    
    # Store the model
    models[target] = model
    
    # Make predictions
    y_pred = model.predict(X_test).flatten()
    predictions[target] = y_pred
    
    # Evaluate the model
    mse = mean_squared_error(y_target_test, y_pred)
    r2 = r2_score(y_target_test, y_pred)
    results[target] = mse
    r2_results[target] = r2
    print(f'Mean Squared Error for {target}: {mse}')
    print(f'R2 for {target}: {r2}')

# Display the results
print("\nModel Performance:")
for target, mse in results.items():
    print(f'{target}: MSE = {mse}')

print("\nModel Performance R2:")
for target, r2 in r2_results.items():
    print(f'{target}: R2 = {r2}')
