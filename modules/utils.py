# Utility functions
import pandas as pd

def calculate_incremented_salary(join_date, basic_salary, rate=0.03):
    try:
        years = (pd.Timestamp.today() - pd.to_datetime(join_date)).days // 365
        increment = basic_salary * rate * years
        return round(basic_salary + increment, 2)
    except Exception:
        return basic_salary  # fallback if date parsing fails
