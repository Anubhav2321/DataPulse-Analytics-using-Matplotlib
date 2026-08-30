from src.data_loader import load_csv
from src.data_cleaner import clean_data, save_cleaned_data
from src.data_processor import get_sales_by_category, get_top_selling_products
from src.statistics import generate_basic_stats
from src.visualizations import plot_category_sales, plot_sales_trend, plot_top_products
from src.insights import generate_analysis_report

def main():
    print("🚀 DataPulse - Data Analysis System Starting...\n")

    # 1. Dataset Loading
    raw_data_path = "data/raw/sales.csv"
    df = load_csv(raw_data_path)

    if df is not None:
        # 2. Data Cleaning
        cleaned_df = clean_data(df)
        processed_data_path = "data/processed/cleaned_sales.csv"
        save_cleaned_data(cleaned_df, processed_data_path)
        
        # 3. Data Processing
        print("\n⚙️  DATA PROCESSING SECTION")
        print("-" * 30)
        category_sales = get_sales_by_category(cleaned_df)
        top_products = get_top_selling_products(cleaned_df)
        
        # 4. Statistical Analysis
        # We store the returned dictionary in 'stats' variable
        stats = generate_basic_stats(cleaned_df)
        
        # 5. Visualizations
        print("\n🎨 VISUALIZATION SECTION")
        print("-" * 30)
        plot_category_sales(category_sales)
        plot_sales_trend(cleaned_df)
        plot_top_products(top_products)
        
        # 6. Final Report Generation
        generate_analysis_report(stats, category_sales, top_products)
        
        print("\n✅ All tasks completed! Check 'visualizations' for charts and 'reports' for the final summary.\n")

if __name__ == "__main__":
    main()