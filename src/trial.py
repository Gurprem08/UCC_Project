import pandas as pd
from sklearn.ensemble import RandomForestRegressor

# Load your data
data = pd.read_csv('Tab_data.csv')

# Define scenarios
scenarios = {
    'Increased agricultural runoff': {'p_NA': data['p_NA'].mean() + data['p_NA'].std()},
    'New wastewater treatment': {'p_CO3': data['p_CO3'].mean() - data['p_CO3'].std()}
}

# Train a model (e.g., RandomForestRegressor)
features = ['pH', 'EC', 'TDS', 'Temperature']
targets = ['p_CO3', 'p_CL', 'p_SO4', 'p_TH', 'p_CA', 'p_MG', 'p_NA', 'WQI']

X = data[features]
y = data[targets]
model = RandomForestRegressor()
model.fit(X, y)

# Simulate scenarios
for scenario, changes in scenarios.items():
    scenario_data = data.copy()
    for param, value in changes.items():
        scenario_data[param] = value
    
    predictions = model.predict(scenario_data[features])
    scenario_data[targets] = predictions
    print(f"Scenario: {scenario}")
    print(scenario_data[targets].describe())
