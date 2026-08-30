import pandas as pd

def get_sales_by_category(df):
    """
    Groups data by Category and calculates total sales and quantity.
    """
    print("[*] Processing: Calculating sales by category...")
    category_sales = df.groupby('Category')[['Total_Sales', 'Quantity']].sum().reset_index()
    # Sort by Total_Sales descending
    category_sales = category_sales.sort_values(by='Total_Sales', ascending=False)
    return category_sales

def get_top_selling_products(df, top_n=3):
    """
    Returns the top selling products based on total sales.
    """
    print(f"[*] Processing: Identifying top {top_n} products...")
    product_sales = df.groupby('Product')['Total_Sales'].sum().reset_index()
    product_sales = product_sales.sort_values(by='Total_Sales', ascending=False).head(top_n)
    return product_sales