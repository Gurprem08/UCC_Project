import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Dropout # type: ignore
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau # type: ignore
from sklearn.metrics import mean_squared_error , r2_score, f1_score , mean_absolute_error, mean_absolute_percentage_error
import joblib

# Load the dataset
data = pd.read_csv('f_dataset.csv')

# Basic parameters used as input
input_features = ["pH", "EC", "TDS", "Temperature"]

# Target parameters to predict
target_features = ['CO3','Cl', 'SO4','TH', 'Ca', 'Mg', 'Na']

# Splitting data into input and target variables
X = data[input_features]
y = data[target_features]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# joblib.dump(scaler, 'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\scaler.pkl')

# Define the DNN model
def create_dnn_model(input_dim, learning_rate = 0.001):
    model = Sequential()
    model.add(Dense(32, input_dim=input_dim, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))  # 20% dropout
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.2))  # 20% dropout
    model.add(Dense(256, activation='relu'))
    model.add(Dense(1))  # Output layer with 1 neuron
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate), loss='mean_squared_error')
    return model

# Dictionary to hold the models and their predictions
models = {}
predictions = {}
results = {}
r2_results ={}
mae_results = {}
mape_results ={}
mse_results = {}

# Train and evaluate a separate model for each target parameter
for target in target_features:
    print(f'Training model for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]
    
    model = create_dnn_model(input_dim=X_train.shape[1])
    # Define early stopping callback
    early_stopping = EarlyStopping(monitor='val_loss', patience=40, restore_best_weights=True)
    reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=20, min_lr=0.0001)

    history = model.fit(X_train, y_target_train, epochs=1000, batch_size=32 ,callbacks = [early_stopping, reduce_lr], validation_split=0.2, verbose=1)
    
    models[target] = model
    y_pred = model.predict(X_test)
    # Ensure all predictions are non-negative
    y_pred = np.maximum(y_pred, 0)


    predictions[target] = y_pred
    mse = mean_squared_error(y_target_test, y_pred)
    mae = mean_absolute_error(y_target_test, y_pred)
    r2 = r2_score(y_target_test, y_pred)
    mape = mean_absolute_percentage_error(y_target_test, y_pred)

    r2_results[target] = r2
    mae_results[target] = mae
    mape_results[target] = mape
    mse_results[target] = mse

    # Ensure all predictions are non-negative
    y_pred = np.maximum(y_pred, 0)
    
    
    print(f"Results for {target}:")
    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")
    print(f"R-squared: {r2}")
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

