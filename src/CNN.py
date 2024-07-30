import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv1D, Flatten
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_percentage_error, mean_absolute_error
import joblib

# Load the dataset
data = pd.read_csv('f_dataset.csv')

# Basic parameters used as input
input_features = ['Temperature', 'EC','TDS', 'pH']

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
# joblib.dump(scaler, 'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\scaler.pkl')


# Reshape input data for CNN
X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))

# Dictionary to hold the models and their predictions
models = {}
predictions = {}
results = {}
r2_results ={}

# Train and evaluate a separate model for each target parameter
for target in target_features:
    print(f'Training model for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]
    
    model = Sequential()
    model.add(Conv1D(32, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(Flatten())
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    model.fit(X_train, y_target_train, epochs=100, batch_size=16, validation_split=0.2, verbose=0)
    
    models[target] = model
    y_pred = model.predict(X_test)
    predictions[target] = y_pred
    mse = mean_squared_error(y_target_test, y_pred)
    r2 = r2_score(y_target_test,y_pred)
    mae = mean_absolute_error(y_target_test,y_pred)
    mape = mean_absolute_percentage_error(y_target_test,y_pred)
    results[target] = mse
    r2_results[target] = r2
    print(f'Mean Squared Error for {target}: {mse}')
    print(f'R2 for {target}: {r2}')
    # joblib.dump(model, f'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\model_{target}.pkl')


# Display the results
print("\nModel Performance:")
for target, mse in results.items():
    print(f'{target}: MSE = {mse}')

print("\nModel Performance r2:")
for target, r2 in r2_results.items():
    print(f'{target}: MSE = {r2}')

print("\nModel Performance MAE:")
for target, r2 in r2_results.items():
    print(f'{target}: MSE = {mae}')


print("\nModel Performance MAPE:")
for target, r2 in r2_results.items():
    print(f'{target}: MSE = {mape}')