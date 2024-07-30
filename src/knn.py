import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings

# Load the dataset
data = pd.read_csv('f_dataset.csv')

# Basic parameters used as input
input_features = ["pH", "EC", "TDS", "Temperature"]

# Target parameters to predict
target_features = ['CO3', 'Cl', 'SO4', 'TH', 'Ca', 'Mg', 'Na']

# Splitting data into input and target variables
X = data[input_features]
y = data[target_features]

# Check for missing values
if X.isnull().values.any() or y.isnull().values.any():
    raise ValueError("Data contains missing values. Please handle them before proceeding.")

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Normalize the data
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Dictionary to store MAE for each target
mae_dict = {}

# Train and evaluate a separate KNN model for each target parameter
for target in target_features:
    print(f'Training KNN for {target}...')
    y_target_train = y_train[target]
    y_target_test = y_test[target]

    # Initialize KNN Regressor
    knn = KNeighborsRegressor()

    # Define the parameter grid for GridSearchCV
    param_grid = {
        'n_neighbors': [3, 5, 7, 9],
        'weights': ['uniform', 'distance'],
        'p': [1, 2]  # 1 for Manhattan distance, 2 for Euclidean distance
    }

    # Create GridSearchCV instance
    grid_search = GridSearchCV(estimator=knn, param_grid=param_grid, cv=3, verbose=1, n_jobs=-1, error_score='raise')

    try:
        # Fit GridSearchCV
        grid_result = grid_search.fit(X_train, y_target_train)

        # Print best parameters and best score
        print(f"Best parameters found for {target}: {grid_result.best_params_}")
        print(f"Best CV score for {target}: {grid_result.best_score_}")

        # Evaluate on test set with best model
        best_knn_model = grid_result.best_estimator_
        y_pred = best_knn_model.predict(X_test)
        mse = mean_squared_error(y_target_test, y_pred)
        mae = mean_absolute_error(y_target_test, y_pred)

        # Store MAE in the dictionary
        mae_dict[target] = mae

        # Print results for the current target
        print(f"Results for {target}:")
        print(f"Mean Squared Error: {mse}")
        print(f"Mean Absolute Error: {mae}")
        print(f"R-squared: {r2_score(y_target_test, y_pred)}")
        print()
    except ValueError as e:
        print(f"Failed to train KNN for {target}: {e}")
        mae_dict[target] = None

# Print dictionary of MAE for all targets
print("MAE Dictionary:")
print(mae_dict)

# Save the best model for each target if needed
# joblib.dump(best_knn_model, f'best_knn_model_{target}.pkl')
