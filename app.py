import streamlit as st
import pandas as pd
import plotly.express as px
from utils.dataloader import fetch_workouts_with_users
from models.fitness_model import train_calorie_models, predict_calories

# --- Load and prep data ---
df = fetch_workouts_with_users()
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by=['user_id', 'date'])

# --- Add week column ---
df['week'] = df['date'].dt.isocalendar().week

# --- Streamlit UI ---
st.title("🏋️‍♂️ FitPro: Fitness Analytics Platfrom")
st.caption("By Ribhay Singh")

# --- Prediction section first ---
st.header("🔥 Predict Calories for New Workout")

duration = st.slider("Duration (minutes)", 20, 90, 45)
age = st.slider("Age", 18, 60, 28)
weight = st.slider("Weight (kg)", 50, 100, 70)
w_type = st.selectbox("Workout Type", ['Cardio', 'Strength', 'Yoga', 'HIIT', 'Pilates'])
gender = st.selectbox("Gender", ['Male', 'Female'])

if st.button("Predict Calories"):
    input_df = pd.DataFrame([{
        'duration': duration,
        'age': age,
        'weight': weight,
        'type': w_type,
        'gender': gender
    }])
    rf_model, xgb_model = train_calorie_models(df)
    predicted_rf = predict_calories(rf_model, input_df)
    predicted_xgb = predict_calories(xgb_model, input_df)

    st.metric("Predicted Calories (RF)", f"{round(predicted_rf)} kcal")
    st.metric("Predicted Calories (XGB)", f"{round(predicted_xgb)} kcal")

st.markdown("---")

# --- User progress ---
st.header("📈 User Progress")

user_id = st.selectbox("Select User ID", df['user_id'].unique())
user_df = df[df['user_id'] == user_id].copy()

# --- Weekly calories ---
weekly_df = user_df.groupby('week', as_index=False).agg({'calories_burned': 'sum'})

# --- Set goal ---
target_goal = st.number_input("Set Your Weekly Target Calories", min_value=500, max_value=50000, value=3000, step=100)

# --- Plotly graph ---
fig = px.bar(
    weekly_df,
    x='week',
    y='calories_burned',
    labels={'week': 'Week Number', 'calories_burned': 'Calories Burned'},
    title='Weekly Calories Burned'
)
fig.update_layout(yaxis_range=[0, max(weekly_df['calories_burned'].max(), target_goal) + 500])

st.plotly_chart(fig, use_container_width=True)

# --- Check goal ---
latest_week_cals = weekly_df['calories_burned'].iloc[-1]
if latest_week_cals >= target_goal:
    st.success("✅ Weekly Goal Achieved! Keep it up!")
else:
    st.warning(f"⚠️ Not there yet: {latest_week_cals}/{target_goal} kcal this week.")

st.metric("Your Weekly Target", f"{int(target_goal)} kcal")
st.metric("Last Week's Total", f"{int(latest_week_cals)} kcal")
