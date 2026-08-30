import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render
from django.http import HttpResponse

def get_base64_graph():
    buffer = io.BytesIO()
    # Transparent background so it merges with the glassmorphism CSS card
    plt.savefig(buffer, format='png', bbox_inches='tight', transparent=True, dpi=120)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()
    return base64.b64encode(image_png).decode('utf-8')

def set_premium_style(ax, title):
    """Applies modern cyberpunk styling to axes."""
    ax.set_facecolor('none')
    ax.tick_params(colors='#94a3b8', labelsize=10)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color('#334155')
    ax.spines['left'].set_color('#334155')
    ax.set_title(title, color='#f8fafc', pad=20, fontsize=14, fontweight='bold')

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('dataset'):
        uploaded_file = request.FILES['dataset']
        file_name = uploaded_file.name
        
        try:
            if file_name.endswith('.csv') or file_name.endswith('.txt'):
                df = pd.read_csv(uploaded_file)
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                return HttpResponse("❌ Unsupported format!")
            
            df.fillna(0, inplace=True)
            sales_col = 'Sales' if 'Sales' in df.columns else 'Total_Sales'
            
            # --- Chart 1: 3D-ish Bar Chart ---
            chart1 = None
            if 'Category' in df.columns and sales_col in df.columns:
                category_sales = df.groupby('Category')[sales_col].sum()
                fig, ax = plt.subplots(figsize=(7, 4.5))
                bars = ax.bar(category_sales.index, category_sales.values, color='#0284c7', edgecolor='#38bdf8', linewidth=1.5, zorder=3)
                
                # Add shadow behind bars
                for bar in bars:
                    bar.set_alpha(0.85)
                ax.grid(color='#334155', linestyle='--', linewidth=0.5, alpha=0.5, zorder=0)
                set_premium_style(ax, 'Revenue by Category')
                chart1 = get_base64_graph()

            # --- Chart 2: 3D Shadow Pie Chart ---
            chart2 = None
            if 'Product' in df.columns and sales_col in df.columns:
                product_sales = df.groupby('Product')[sales_col].sum().nlargest(5)
                fig, ax = plt.subplots(figsize=(7, 4.5))
                colors = ['#0284c7', '#0369a1', '#075985', '#0ea5e9', '#38bdf8']
                explode = [0.08] + [0] * (len(product_sales) - 1) # Separate top product
                
                wedges, texts, autotexts = ax.pie(
                    product_sales, autopct='%1.1f%%', colors=colors, 
                    explode=explode, shadow=True, startangle=140, 
                    textprops={'color':"w", 'weight':'bold', 'fontsize': 10}
                )
                # Premium label styling
                for text in texts:
                    text.set_color('#f8fafc')
                ax.set_title('Top Products Share', color='#f8fafc', pad=20, fontsize=14, fontweight='bold')
                chart2 = get_base64_graph()

            # --- Chart 3: Neon Glowing Area Chart ---
            chart3 = None
            if 'Date' in df.columns and sales_col in df.columns:
                df['Date'] = pd.to_datetime(df['Date'])
                date_sales = df.groupby('Date')[sales_col].sum()
                
                fig, ax = plt.subplots(figsize=(11, 4.5))
                # Main neon line
                ax.plot(date_sales.index, date_sales.values, color='#38bdf8', marker='o', markersize=6, linewidth=2.5, zorder=3)
                # Glowing fill area
                ax.fill_between(date_sales.index, date_sales.values, color='#0284c7', alpha=0.2, zorder=2)
                
                ax.grid(color='#334155', linestyle=':', linewidth=1, alpha=0.7, zorder=0)
                set_premium_style(ax, 'Daily Sales Trend')
                chart3 = get_base64_graph()

            context = {
                'file_name': file_name,
                'total_rows': df.shape[0],
                'total_cols': df.shape[1],
                'chart1': chart1,
                'chart2': chart2,
                'chart3': chart3,
                'data_html': df.head(10).to_html(classes="data-table", index=False)
            }
            return render(request, 'result.html', context)
            
        except Exception as e:
            return HttpResponse(f"❌ Error processing file: {e}")
            
    return render(request, 'index.html')