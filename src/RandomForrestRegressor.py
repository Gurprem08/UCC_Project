import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
import joblib

# Load the dataset
data = pd.read_csv('F_dataset.csv')

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
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# joblib.dump(scaler, 'scaler.pkl')

# Train and evaluate a separate model for each target parameter
for target in target_features:
    print(f'Training model for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]

    # Initialize the Random Forest Regressor
    rf_model = RandomForestRegressor(random_state=42)

    # Define the parameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [None, 10, 20, 30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }

    # Create GridSearchCV instance
    grid_search = GridSearchCV(estimator=rf_model, param_grid=param_grid, cv=3, verbose=1, n_jobs=-1)

    # Fit GridSearchCV
    grid_result = grid_search.fit(X_train, y_target_train)

    # Print best parameters and best score
    print(f"Best parameters found for {target}: {grid_result.best_params_}")
    print(f"Best CV score for {target}: {grid_result.best_score_}")

    # Evaluate on test set with best model
    best_rf_model = grid_result.best_estimator_
    y_pred = best_rf_model.predict(X_test)
    mse = mean_squared_error(y_target_test, y_pred)
    mae = mean_absolute_error(y_target_test, y_pred)
    r2 = r2_score(y_target_test, y_pred)
    mae_dict ={}
    mae_dict[target] = mae
    print(f"Results for {target}:")
    print(f"Mean Squared Error: {mse}")
    print(f"Mean Absolute Error: {mae}")
    print(f"R-squared: {r2}")
print(mae_dict)
# Save the best model for each target if needed
# joblib.dump(best_rf_model, f'best_rf_model_{target}.pkl')
