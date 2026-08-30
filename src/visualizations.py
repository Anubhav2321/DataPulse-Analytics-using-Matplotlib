import matplotlib.pyplot as plt
import os

# Ensure the visualizations directory exists
SAVE_DIR = "visualizations"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def plot_category_sales(category_df):
    """Generates and saves a bar chart for category-wise sales."""
    print("[*] Generating Bar Chart: Category-wise Sales...")
    plt.figure(figsize=(8, 5))
    
    # Plotting the bar chart
    plt.bar(category_df['Category'], category_df['Total_Sales'], color=['#4C72B0', '#55A868', '#C44E52'])
    
    plt.title('Total Sales by Category', fontsize=14)
    plt.xlabel('Category', fontsize=12)
    plt.ylabel('Total Sales (₹)', fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    # Save the chart
    save_path = os.path.join(SAVE_DIR, 'category_sales_bar.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close() # Close the figure to free memory
    print(f"[✓] Saved chart at: {save_path}")

def plot_sales_trend(df):
    """Generates and saves a line chart for sales trends over time."""
    print("[*] Generating Line Chart: Daily Sales Trend...")
    
    # Group by date to get daily total sales
    daily_sales = df.groupby('Date')['Total_Sales'].sum().reset_index()
    
    plt.figure(figsize=(10, 5))
    plt.plot(daily_sales['Date'], daily_sales['Total_Sales'], marker='o', linestyle='-', color='#C44E52', linewidth=2)
    
    plt.title('Daily Sales Trend', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Total Sales (₹)', fontsize=12)
    plt.xticks(rotation=45) # Rotate dates for better readability
    plt.grid(True, linestyle='--', alpha=0.5)
    
    save_path = os.path.join(SAVE_DIR, 'daily_sales_trend.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Saved chart at: {save_path}")

def plot_top_products(top_products_df):
    """Generates and saves a pie chart for top selling products."""
    print("[*] Generating Pie Chart: Top Selling Products...")
    plt.figure(figsize=(6, 6))
    
    colors = ['#DD8452', '#8172B3', '#937860']
    plt.pie(top_products_df['Total_Sales'], labels=top_products_df['Product'], autopct='%1.1f%%', startangle=140, colors=colors)
    
    plt.title('Top Selling Products Share', fontsize=14)
    
    save_path = os.path.join(SAVE_DIR, 'top_products_pie.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[✓] Saved chart at: {save_path}")