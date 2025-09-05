# Excel data loading logic
import pandas as pd

def load_cf_data(filepath):
    try:
        df = pd.read_excel(filepath)
        df = df.dropna(subset=["Name of School", "Date of Joining in the ICT", "Basic Salary"])
        return df
    except Exception as e:
        raise RuntimeError(f"Error loading data: {e}")
