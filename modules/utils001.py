# Utility functions
import pandas as pd

def calculate_incremented_salary(join_date, basic_salary, rate=0.03):
    try:
        years = (pd.Timestamp.today() - pd.to_datetime(join_date)).days // 365
        increment = basic_salary * rate * years
        return round(basic_salary + increment, 2)
    except Exception:
        return basic_salary  # fallback if date parsing fails

# modules/utils.py

def get_available_salary_components(df, expected_cols):
    """
    Returns a list of salary component columns that exist in the DataFrame.
    """
    return [col for col in expected_cols if col in df.columns]
