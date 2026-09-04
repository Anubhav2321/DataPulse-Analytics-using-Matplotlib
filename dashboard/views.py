import pandas as pd
import json
import os
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from groq import Groq

# Initialize Groq Client (using the key from settings.py)
client = Groq(api_key=settings.GROQ_API_KEY) if hasattr(settings, 'GROQ_API_KEY') else None

def get_universal_insights(df, num_col, cat_col, date_col):
    """Generates dynamic, invisible AI insights using Groq."""
    if not client:
        return "<b>System Error:</b> Analytical engine offline. Please verify API configuration."

    try:
        # 1. Statistical Fingerprinting (Creating a summary to send, avoiding raw data limits)
        total_val = df[num_col].sum()
        mean_val = df[num_col].mean()
        top_cat = df.groupby(cat_col)[num_col].sum().idxmax() if cat_col else "N/A"
        
        time_trend = "N/A"
        if date_col:
            try:
                time_trend = f"From {df[date_col].min()} to {df[date_col].max()}"
            except:
                pass

        data_summary = f"""
        Dataset Size: {len(df)} records
        Primary Metric: {num_col}
        Total {num_col}: {total_val:,.2f}
        Average {num_col}: {mean_val:,.2f}
        Top Performing Segment ({cat_col}): {top_cat}
        Timeframe: {time_trend}
        """

        # 2. Strict Prompt Engineering for "Invisible AI"
        system_prompt = """You are the core analytical engine of 'DataPulse'. 
        Analyze the statistical summary and generate a strict, professional business report.
        CRITICAL RULES:
        - Do NOT use conversational filler, greetings, or reveal you are an AI.
        - Sound like an automated enterprise system outputting a terminal report.
        - Format your output EXACTLY with these three sections using HTML tags:
        
        <b>Executive Summary:</b> [1 concise sentence summarizing the overall performance]
        <br><br><b>Anomaly & Risk Detection:</b> [1 sentence identifying a potential outlier, dependency, or risk based on the data]
        <br><br><b>Actionable Forecast:</b> [1 sentence strategic recommendation for the user]"""

        # 3. API Call to Groq (Using Mixtral for fast, accurate logical reasoning)
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data_summary}
            ],
            temperature=0.2,
            max_tokens=350,
        )
        
        return completion.choices[0].message.content
    except Exception as e:
        return f"<b>System Diagnostics:</b><br>Analysis complete. Use visualizations to monitor metrics. (Error: {str(e)})"


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
            
            # AUTO-DETECT COLUMNS
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
            categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
            
            date_col = None
            for col in df.columns:
                if 'date' in col.lower() or 'time' in col.lower() or 'day' in col.lower() or 'year' in col.lower():
                    date_col = col
                    break
            
            if not numeric_cols:
                df['Count'] = 1
                numeric_cols = ['Count']
                
            primary_num = numeric_cols[0] 
            primary_cat = categorical_cols[0] if categorical_cols else None 
            secondary_cat = categorical_cols[1] if len(categorical_cols) > 1 else primary_cat 

            # --- AI Insights Generate (Updated to pass date_col) ---
            ai_insights_text = get_universal_insights(df, primary_num, primary_cat, date_col)
            
            # --- Chart Data Preparation ---
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
                    pass 

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