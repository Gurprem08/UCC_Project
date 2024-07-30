import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Load the dataset
data = pd.read_csv('f_dataset.csv')

# Basic parameters used as input
input_features = ["Temperature", 'EC', 'TDS', 'pH']

# Advanced parameters to predict and then use in WQI calculation
target_features = ['CO3', 'Cl', 'SO4', 'TH', 'Ca', 'Mg', 'Na']

# Splitting data into input and target variables
X = data[input_features]
y = data[target_features]

# Polynomial Features
poly = PolynomialFeatures(degree=2, interaction_only=True)
X_poly = poly.fit_transform(X)

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_poly, y, test_size=0.2, random_state=42)

# Standardize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Function to create DNN model
def create_dnn_model(input_dim, learning_rate=0.001):
    model = Sequential()
    model.add(Dense(64, input_dim=input_dim, activation='relu', kernel_regularizer='l2'))
    model.add(Dropout(0.2))
    model.add(Dense(128, activation='relu', kernel_regularizer='l2'))
    model.add(Dropout(0.2))
    model.add(Dense(256, activation='relu', kernel_regularizer='l2'))
    model.add(Dropout(0.2))
    model.add(Dense(512, activation='relu', kernel_regularizer='l2'))
    model.add(Dense(1, activation='relu'))  # ReLU activation in output layer
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Dictionary to hold the models and their predictions
models = {}
predictions = {}
results = {}
r2_results ={}
mae_results = {}
mape_results ={}
mse_results = {}

for target in target_features:
    print(f'Training model for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]
    
    # Create the model
    model = create_dnn_model(X_train.shape[1])
    
    # Define early stopping and learning rate reduction callbacks
    early_stopping = EarlyStopping(monitor='val_loss', patience=20, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=20, min_lr=0.0001)
    
    # Train the model with early stopping and learning rate reduction
    history = model.fit(X_train, y_target_train, epochs=1000, batch_size=32, validation_split=0.2, verbose=1, callbacks=[early_stopping, reduce_lr])
    
    # Evaluate the model
    y_pred = model.predict(X_test)
    
    # Ensure all predictions are non-negative
    y_pred = np.maximum(y_pred, 0)
    
    # Calculate metrics
    mse = mean_squared_error(y_target_test, y_pred)
    r2 = r2_score(y_target_test, y_pred)
    mae = mean_absolute_error(y_target_test, y_pred)
    
    r2_results[target] = r2
    mae_results[target] = mae
    mse_results[target] = mse
    
    print(f"Model Performance - MSE: {mse}, R2: {r2}, MAE: {mae}")
    
    # Store the predictions
    predictions[target] = y_pred

# If still interested in MAPE, handle small target values
def safe_mape(y_true, y_pred):
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100

# Calculate MAPE for each target feature
mape_values = {}
for target in target_features:
    mape_values[target] = safe_mape(y_test[target].values, predictions[target])

# Display the results
print("\nModel Performance:")
for target, mse in mse_results.items():
    print(f'{target}: MSE = {mse}')

print("\nModel Performance R2:")
for target, r2 in r2_results.items():
    print(f'{target}: R2 = {r2}')

print("\nModel Performance MAE:")
for target, mae in mae_results.items():
    print(f'{target}: MAE = {mae}')

print("\nModel Performance MAPE:")
for target, mape in mape_values.items():
    print(f'{target}: MAPE = {mape}')
