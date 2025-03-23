import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Load dataset
df = pd.read_csv(r"D:\Projects\Data_Analytics\Ps_analysis\data\processed\Teaching_metrics.csv")
# Drop non-numeric and unnecessary columns
df.drop(columns=['Faculty_ID', 'Faculty_Name', 'Department'], inplace=True)

# Handle missing values
df.fillna(df.mean(), inplace=True) # Filling missing values with column mean

# print(df)

X = df.drop(columns=['Pass_Percentage'])  # Features
y = df['Pass_Percentage']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model performance
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f'Mean Absolute Error: {mae:.2f}')
print(f'R² Score: {r2:.2f}')

import joblib
joblib.dump(model, 'pass_percentage_model.pkl')
print("✅ Model saved as pass_percentage_model.pkl")
