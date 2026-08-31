import pandas as pd
import json
from django.shortcuts import render
from django.http import HttpResponse

def get_universal_insights(df, num_col, cat_col):
    """It will generate dynamic insights based on any dataset."""
    try:
        total_val = df[num_col].sum()
        insight = f"Data Scan Complete: We analyzed {len(df)} records. "
        insight += f"The primary numerical metric identified is '{num_col}', with a total aggregated value of {total_val:,.2f}. "
        
        if cat_col:
            top_cat = df.groupby(cat_col)[num_col].sum().idxmax()
            insight += f"Among the '{cat_col}' segments, '{top_cat}' holds the highest concentration. "
            
        insight += "Recommendation: Use the visualizations below to monitor key performance indicators and identify outliers across these metrics."
        return insight
    except Exception as e:
        return "Dataset analyzed successfully. Please review the visual charts for detailed breakdowns."

def upload_file(request):
    if request.method == 'POST' and request.FILES.get('dataset'):
        uploaded_file = request.FILES['dataset']
        file_name = uploaded_file.name
        
        try:
            # 1. File Read
            if file_name.endswith('.csv') or file_name.endswith('.txt'):
                df = pd.read_csv(uploaded_file)
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(uploaded_file)
            else:
                return HttpResponse("❌ Unsupported format!")
            
            df.fillna(0, inplace=True)
            
            # 2. AUTO-DETECT COLUMNS (Magic Logic)
            # Searching the number column
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            # Searching Text/Category Columns
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            # Searching Date/Time Columns
            date_col = None
            for col in df.columns:
                if 'date' in col.lower() or 'time' in col.lower() or 'day' in col.lower() or 'year' in col.lower():
                    date_col = col
                    break
            
            # If no numeric column is found, create a Count column
            if not numeric_cols:
                df['Count'] = 1
                numeric_cols = ['Count']
                
            primary_num = numeric_cols[0] # The first column will be targeted for the graph.
            primary_cat = categorical_cols[0] if categorical_cols else None # The first categorical column
            secondary_cat = categorical_cols[1] if len(categorical_cols) > 1 else primary_cat # The second categorical column (for pie charts)

            # --- AI Insights Generate ---
            ai_insights_text = get_universal_insights(df, primary_num, primary_cat)
            
            # --- Chart Data Preparation (Dynamic) ---
            bar_data = {"labels": [], "values": [], "title": ""}
            if primary_cat:
                bar_df = df.groupby(primary_cat)[primary_num].sum().nlargest(10).reset_index()
                bar_data["labels"] = bar_df[primary_cat].astype(str).tolist()
                bar_data["values"] = bar_df[primary_num].tolist()
                bar_data["title"] = f"Total {primary_num} by {primary_cat}"

            pie_data = {"labels": [], "values": [], "title": ""}
            if secondary_cat:
                pie_df = df.groupby(secondary_cat)[primary_num].sum().nlargest(5).reset_index()
                pie_data["labels"] = pie_df[secondary_cat].astype(str).tolist()
                pie_data["values"] = pie_df[primary_num].tolist()
                pie_data["title"] = f"Top 5 {secondary_cat} share in {primary_num}"

            trend_data = {"labels": [], "values": [], "title": ""}
            if date_col:
                try:
                    df[date_col] = pd.to_datetime(df[date_col])
                    trend_df = df.groupby(df[date_col].dt.strftime('%Y-%m-%d'))[primary_num].sum().reset_index()
                    trend_data["labels"] = trend_df[date_col].tolist()
                    trend_data["values"] = trend_df[primary_num].tolist()
                    trend_data["title"] = f"{primary_num} Trend over {date_col}"
                except:
                    pass # If the date conversion fails, the area chart will be empty

            context = {
                'file_name': file_name,
                'total_rows': df.shape[0],
                'total_cols': df.shape[1],
                'data_html': df.head(10).to_html(classes="data-table", index=False),
                'bar_data': json.dumps(bar_data),
                'pie_data': json.dumps(pie_data),
                'trend_data': json.dumps(trend_data),
                'ai_insights': ai_insights_text,
            }
            return render(request, 'result.html', context)
            
        except Exception as e:
            return HttpResponse(f"❌ Error processing file: {str(e)}")
            
    return render(request, 'index.html')