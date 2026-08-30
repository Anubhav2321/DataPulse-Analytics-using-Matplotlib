import pandas as pd
import os

def load_csv(file_path):
    """This function will read the CSV file and return a DataFrame.।"""
    if not os.path.exists(file_path):
        print(f"❌ Error: '{file_path}' file not found!")
        return None
    
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Success: '{file_path}' loaded successfully!")
        return df
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None

def display_basic_info(df):
    """This function will display basic information about the dataset."""
    if df is not None:
        print("\n" + "="*40)
        print("📊 DATASET INFORMATION")
        print("="*40)
        print(f"Total Rows: {df.shape[0]}")
        print(f"Total Columns: {df.shape[1]}")
        print(f"\nColumns: {', '.join(df.columns)}")
        print("\nData Types:")
        print(df.dtypes)
        print("\nFirst 3 Rows:")
        print(df.head(3))
        print("="*40 + "\n")