import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error
from tensorflow.keras.callbacks import EarlyStopping # type: ignore
import joblib

# Load the dataset
data = pd.read_csv('Data_3years.csv')

# Basic parameters used as input
input_features = ['Temperature', 'EC', 'TDS', 'pH']

# Target parameters to predict
target_features = ['CO3', 'Cl', 'SO4', 'TH', 'Ca', 'Mg', 'Na']

# Splitting data into input and target variables
X = data[input_features]
y = data[target_features]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Save the scaler
# joblib.dump(scaler, 'scaler.pkl')
# joblib.dump(scaler, 'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\scaler.pkl')


# Reshape input data for LSTM (samples, timesteps, features)
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# Dictionary to hold the models and their predictions
models = {}
predictions = {}
results = {}
r2_results = {}
mae_results = {}
mape_results ={}

# Train and evaluate a separate model for each target parameter
for target in target_features:
    print(f'Training model for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]
    
    model = Sequential()
    model.add(LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2]), activation='relu', return_sequences=True))
    model.add(Dropout(0.2))  # 20% dropout
    model.add(LSTM(128, activation='relu', return_sequences=True))
    model.add(Dropout(0.2))  # 20% dropout
    model.add(LSTM(256, activation='relu'))
    model.add(Dense(1, activation='relu'))  # Output layer with 1 neuron
    model.compile(optimizer='adam', loss='mse')
    
    # Define early stopping callback
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)

    # Fit the model
    model.fit(X_train, y_target_train, epochs=100, batch_size=16, callbacks = [early_stopping],validation_split=0.2, verbose=1)
    
    models[target] = model
    y_pred = model.predict(X_test)
    predictions[target] = y_pred
    mse = mean_squared_error(y_target_test, y_pred)
    r2 = r2_score(y_target_test, y_pred)
    mae = mean_absolute_error(y_target_test, y_pred)
    mape = mean_absolute_percentage_error(y_target_test, y_pred)
    
    results[target] = mse
    r2_results[target] = r2
    mae_results[target] = mae
    mape_results[target] = mape

    print(f'Mean Squared Error for {target}: {mse}')
    print(f'R2 for {target}: {r2}')
    print(f'Mean Absolute Error for {target}: {mae}')
    print(f'Mean Absolute Percnetage Error for {target}: {mape}')
    # joblib.dump(model, f'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\model_{target}.pkl')


# Display the results
print("\nModel Performance:")
for target, mse in results.items():
    print(f'{target}: MSE = {mse}')

print("\nModel Performance R2:")
for target, r2 in r2_results.items():
    print(f'{target}: R2 = {r2}')

print("\nModel Performance MAE:")
for target, mae in mae_results.items():
    print(f'{target}: MAE = {mae}')

print("\nModel Performance MAPE:")
for target, mape in mape_results.items():
    print(f'{target}: MAPE = {mape}')
