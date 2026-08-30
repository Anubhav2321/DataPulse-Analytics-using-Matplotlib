import pandas as pd

def generate_basic_stats(df):
    """
    Calculates and prints basic statistical metrics from the dataset.
    """
    print("\n" + "="*40)
    print("📈 STATISTICAL INSIGHTS")
    print("="*40)
    
    total_sales = df['Total_Sales'].sum()
    average_sales = df['Total_Sales'].mean()
    total_items_sold = df['Quantity'].sum()
    max_sale_value = df['Total_Sales'].max()
    min_sale_value = df['Total_Sales'].min()
    
    stats = {
        "Total Revenue": f"₹ {total_sales:,.2f}",
        "Average Sale Price": f"₹ {average_sales:,.2f}",
        "Total Items Sold": int(total_items_sold),
        "Highest Single Sale": f"₹ {max_sale_value:,.2f}",
        "Lowest Single Sale": f"₹ {min_sale_value:,.2f}"
    }
    
    for key, value in stats.items():
        print(f" - {key:<20}: {value}")
        
    print("="*40 + "\n")
    return stats