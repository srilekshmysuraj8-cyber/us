import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

if not os.path.exists('model'): os.makedirs('model')
df = pd.read_csv('datasets/HISTORICAL_DATA.csv')
X = df[['Age', 'Doctor_ID', 'Time_of_Day', 'Queue_Size']]
y = df['Actual_Consultation_Time']

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X, y)
joblib.dump(model, 'model/wait_time_model.pkl')
print("✅ AI Model Trained!")