import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error, mean_absolute_percentage_error

# Load the dataset
data = pd.read_csv('f_dataset.csv')

# Basic parameters used as input
input_features = ["pH", "EC", "TDS", "Temperature"]

# Target parameters to predict
target_features = ['CO3', 'Cl', 'SO4', 'TH', 'Ca', 'Mg', 'Na']

# Splitting data into input and target variables
X = data[input_features]
y = data[target_features]

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define the DNN model
def create_dnn_model(input_dim, learning_rate=0.001):
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

# Train and evaluate a separate model for each target parameter (DNN and Linear Regression)
models = {}
predictions = {}
results = {}
r2_results = {}
mae_results = {}
mape_results = {}
mse_results = {}

for target in target_features:
    print(f'Training models for {target}...')
    
    # Train DNN model
    dnn_model = create_dnn_model(input_dim=X_train.shape[1])
    history = dnn_model.fit(X_train, y_train[target], epochs=1000, batch_size=32, verbose=0,
                            validation_split=0.2, callbacks=[tf.keras.callbacks.EarlyStopping(patience=40, restore_best_weights=True)])

    # Train Linear Regression model
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train[target])
    
    # Store models
    models[target] = {'DNN': dnn_model, 'Linear Regression': lr_model}

    # Make predictions
    y_pred_dnn = dnn_model.predict(X_test)
    y_pred_lr = lr_model.predict(X_test)

    # Evaluate DNN model
    mse_dnn = mean_squared_error(y_test[target], y_pred_dnn)
    mae_dnn = mean_absolute_error(y_test[target], y_pred_dnn)
    r2_dnn = r2_score(y_test[target], y_pred_dnn)
    mape_dnn = mean_absolute_percentage_error(y_test[target], y_pred_dnn)

    # Evaluate Linear Regression model
    mse_lr = mean_squared_error(y_test[target], y_pred_lr)
    mae_lr = mean_absolute_error(y_test[target], y_pred_lr)
    r2_lr = r2_score(y_test[target], y_pred_lr)
    mape_lr = mean_absolute_percentage_error(y_test[target], y_pred_lr)

    # Store results
    results[target] = {'DNN': mse_dnn, 'Linear Regression': mse_lr}
    r2_results[target] = {'DNN': r2_dnn, 'Linear Regression': r2_lr}
    mae_results[target] = {'DNN': mae_dnn, 'Linear Regression': mae_lr}
    mape_results[target] = {'DNN': mape_dnn, 'Linear Regression': mape_lr}
    mse_results[target] = {'DNN': mse_dnn, 'Linear Regression': mse_lr}

    print(f"\nResults for {target}:")
    print(f"DNN - Mean Squared Error: {mse_dnn}, R-squared: {r2_dnn}")
    print(f"Linear Regression - Mean Squared Error: {mse_lr}, R-squared: {r2_lr}")

# Display the results
print("\nModel Performance MSE:")
for target, mse in results.items():
    print(f'{target}: MSE - DNN = {mse["DNN"]}, Linear Regression = {mse["Linear Regression"]}')

print("\nModel Performance R2:")
for target, r2 in r2_results.items():
    print(f'{target}: R2 - DNN = {r2["DNN"]}, Linear Regression = {r2["Linear Regression"]}')

print("\nModel Performance MAE:")
for target, mae in mae_results.items():
    print(f'{target}: MAE - DNN = {mae["DNN"]}, Linear Regression = {mae["Linear Regression"]}')

print("\nModel Performance MAPE:")
for target, mape in mape_results.items():
    print(f'{target}: MAPE - DNN = {mape["DNN"]}, Linear Regression = {mape["Linear Regression"]}')
