import psycopg2
import pandas as pd

def fetch_users():
    conn = psycopg2.connect(
        dbname="fitpro",
        user="ribhay",
        host="localhost",
        password="",
        port="5432"
    )
    df = pd.read_sql("SELECT * FROM Users;", conn)
    conn.close()
    return df

def fetch_workouts():
    conn = psycopg2.connect(
        dbname="fitpro",
        user="ribhay",
        host="localhost",
        password="",
        port="5432"
    )
    df = pd.read_sql("SELECT * FROM Workouts;", conn)
    conn.close()
    return df

def fetch_goals():
    conn = psycopg2.connect(
        dbname="fitpro",
        user="ribhay",
        host="localhost",
        password="",
        port="5432"
    )
    df = pd.read_sql("SELECT * FROM Goals;", conn)
    conn.close()
    return df

def fetch_workouts_with_users():
    conn = psycopg2.connect(
        dbname="fitpro",
        user="ribhay",
        host="localhost",
        password="",
        port="5432"
    )
    query = """
        SELECT w.*, u.age, u.gender, u.weight
        FROM Workouts w
        JOIN Users u ON w.user_id = u.user_id;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def fetch_weekly_calories():
    conn = psycopg2.connect(
        dbname="fitpro",
        user="ribhay",
        host="localhost",
        password="",
        port="5432"
    )
    query = """
        SELECT 
            user_id,
            DATE_TRUNC('week', date) AS week_start,
            SUM(calories_burned) AS total_calories
        FROM Workouts
        GROUP BY user_id, week_start
        ORDER BY user_id, week_start;
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df
