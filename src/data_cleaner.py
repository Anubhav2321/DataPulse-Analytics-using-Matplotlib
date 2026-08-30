import pandas as pd

def clean_data(df):
    """Main function to clean the dataset"""
    print("\n🧹 Starting Data Cleaning Process...")
    
    # 1. Removing duplicate rows
    initial_rows = len(df)
    df = df.drop_duplicates()
    print(f"[-] Removed {initial_rows - len(df)} duplicate row(s).")
    
    # 2. Converting Date column to datetime format
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        print("[✓] Converted 'Date' column to datetime format.")
        
    # 3. Handling missing values
    # If the quantity is left blank, I will set it to a default of 1.
    if 'Quantity' in df.columns:
        df['Quantity'] = df['Quantity'].fillna(1)
    
    # If the price is left blank, I will set it to a default of 0.
    if 'Total_Sales' in df.columns and 'Price' in df.columns and 'Quantity' in df.columns:
        df['Total_Sales'] = df['Total_Sales'].fillna(df['Price'] * df['Quantity'])
    
    print("[✓] Handled missing values.")
    print("✨ Data cleaning completed successfully!\n")
    
    return df

def save_cleaned_data(df, output_path):
    """Function to save the cleaned data to a CSV file"""
    try:
        df.to_csv(output_path, index=False)
        print(f"✅ Cleaned dataset saved to: {output_path}\n")
    except Exception as e:
        print(f"❌ Error saving cleaned data: {e}\n")