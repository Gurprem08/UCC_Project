import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
import numpy as np
import joblib



# Load your dataset
data = pd.read_csv('f_dataset.csv')

# Assuming your target variables are named 'CO3', 'HCO3', 'Cl', 'SO4', 'NO3', 'TH', 'Ca', 'Mg', 'Na', 'K', 'F'
# Drop the target variables from the features
X = data.drop(['CO3','Cl', 'SO4','TH', 'Ca', 'Mg', 'Na'], axis=1)
y = data[['CO3','Cl', 'SO4','TH', 'Ca', 'Mg', 'Na']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the data using MinMaxScaler
scaler = MinMaxScaler()
X_train_norm = scaler.fit_transform(X_train)
X_test_norm = scaler.transform(X_test)

# Build the ANN model
model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train_norm.shape[1],)),
    Dense(64, activation='relu'),
    Dense(7)  # 7 output neurons for the 7 parameters
])

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train_norm, y_train, epochs=100, batch_size=32, verbose=1)

# Evaluate the model
train_loss = model.evaluate(X_train_norm, y_train, verbose=0)
test_loss = model.evaluate(X_test_norm, y_test, verbose=0)
print(f"Train Loss: {train_loss}, Test Loss: {test_loss}")

# Predict on test data
y_pred = model.predict(X_test_norm)

# Calculate R2 score and MSE for each predictive parameter
parameter_names = ['CO3','Cl', 'SO4','TH', 'Ca', 'Mg', 'Na']
for i, parameter in enumerate(parameter_names):
    r2 = r2_score(y_test[parameter], y_pred[:, i])
    mse = mean_squared_error(y_test[parameter], y_pred[:, i])
    print(f"{parameter}: R2 = {r2}, MSE = {mse}")

joblib.dump(model, 'D:\coding\java script\React Project- Articles project\Project UCC\water-quality-predictions\src\model1.pkl')

