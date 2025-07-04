import psycopg2
import random
from datetime import datetime, timedelta

conn = psycopg2.connect(
    dbname="fitpro",
    user="ribhay",
    host="localhost",
    password="",
    port="5432"
)
cursor = conn.cursor()

workout_types = ['Cardio', 'Strength', 'Yoga', 'HIIT', 'Pilates']

start_date = datetime(2025, 6, 1)

for i in range(50):  # Generate 50 workouts
    user_id = random.choice([1, 2])
    w_type = random.choice(workout_types)
    duration = random.randint(20, 90)  # minutes
    date = start_date + timedelta(days=random.randint(0, 30))

    # Assign multiplier based on workout type
    if w_type == 'Cardio':
        multiplier = random.uniform(10, 12)
    elif w_type == 'Strength':
        multiplier = random.uniform(8, 10)
    elif w_type == 'Yoga':
        multiplier = random.uniform(4, 6)
    elif w_type == 'HIIT':
        multiplier = random.uniform(12, 14)
    else:  # Pilates
        multiplier = random.uniform(5, 7)

    calories = duration * multiplier

    cursor.execute(
        "INSERT INTO Workouts (user_id, type, duration, date, calories_burned) VALUES (%s, %s, %s, %s, %s)",
        (user_id, w_type, duration, date.date(), calories)
    )

conn.commit()
cursor.close()
conn.close()

print("✅ Inserted 50 realistic synthetic workouts successfully!")
