# trained using both RandomForest and XGBoost.

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import r2_score

def train_calorie_models(df):
    df = pd.get_dummies(df, columns=['type', 'gender'], drop_first=True)

    features = df[['duration', 'age', 'weight'] + [col for col in df.columns if 'type_' in col or 'gender_' in col]]
    target = df['calories_burned']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # --- Random Forest ---
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    rf_pred = rf_model.predict(X_test)
    rf_score = r2_score(y_test, rf_pred)
    print(f"🌳 Random Forest R² score: {round(rf_score, 2)}")

    # --- XGBoost ---
    xgb_model = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
    xgb_model.fit(X_train, y_train)
    xgb_pred = xgb_model.predict(X_test)
    xgb_score = r2_score(y_test, xgb_pred)
    print(f"⚡ XGBoost R² score: {round(xgb_score, 2)}")

    return rf_model, xgb_model


def predict_calories(model, workout_input_df):
    workout_input_df = pd.get_dummies(workout_input_df, columns=['type', 'gender'], drop_first=True)

    expected_cols = model.feature_names_in_
    for col in expected_cols:
        if col not in workout_input_df.columns:
            workout_input_df[col] = 0

    workout_input_df = workout_input_df[expected_cols]

    prediction = model.predict(workout_input_df)[0]
    return prediction
