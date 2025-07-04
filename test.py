from utils.dataloader import fetch_workouts_with_users, fetch_goals
from models.fitness_model import train_calorie_models, predict_calories
import pandas as pd

# Fetch data
df_workouts = fetch_workouts_with_users()
df_goals = fetch_goals()

# Merge workouts and goals
df = pd.merge(df_workouts, df_goals, on='user_id', how='left')
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['user_id', 'date'])
df['cumulative_calories'] = df.groupby('user_id')['calories_burned'].cumsum()
df['goal_achieved'] = df['cumulative_calories'] >= df['target_value']

print(df[['user_id', 'date', 'calories_burned', 'cumulative_calories', 'target_value', 'goal_achieved']].head())

# Train both models
rf_model, xgb_model = train_calorie_models(df)

# Example new workout
new_workout = pd.DataFrame([{
    'duration': 45,
    'age': 28,
    'weight': 70,
    'type': 'Cardio',
    'gender': 'Male'
}])

predicted_calories_rf = predict_calories(rf_model, new_workout)
predicted_calories_xgb = predict_calories(xgb_model, new_workout)

print(f"🔥 Predicted calories burned (RF): {round(predicted_calories_rf)} kcal")
print(f"⚡ Predicted calories burned (XGB): {round(predicted_calories_xgb)} kcal")
