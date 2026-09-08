import pandas as pd
import numpy as np
import json
import re
import os
import io
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server-side rendering
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch, Wedge
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from groq import Groq

# ReportLab imports for PDF generation
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import inch, mm, cm
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib import colors as rl_colors

# ═══════════════════════════════════════════════════════════════
# GROQ CLIENT INITIALIZATION
# ═══════════════════════════════════════════════════════════════
client = Groq(api_key=settings.GROQ_API_KEY) if hasattr(settings, 'GROQ_API_KEY') and settings.GROQ_API_KEY else None

GROQ_MODEL = "qwen/qwen3.8-27b"
MAX_ROWS_CLIENT = 500  # Max rows to serialize for client-side operations


def _strip_think_tags(text):
    """Strip <think>...</think> reasoning blocks from model output."""
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()


# ═══════════════════════════════════════════════════════════════
# HELPER: AI INSIGHT GENERATOR
# ═══════════════════════════════════════════════════════════════
def get_universal_insights(df, num_col, cat_col, date_col):
    """Generates dynamic AI insights using Groq."""
    if not client:
        return "<b>System Error:</b> Analytical engine offline. Please verify API configuration."

    try:
        total_val = df[num_col].sum()
        mean_val = df[num_col].mean()
        top_cat = df.groupby(cat_col)[num_col].sum().idxmax() if cat_col else "N/A"

        time_trend = "N/A"
        if date_col:
            try:
                time_trend = f"From {df[date_col].min()} to {df[date_col].max()}"
            except Exception:
                pass

        data_summary = f"""
        Dataset Size: {len(df)} records
        Primary Metric: {num_col}
        Total {num_col}: {total_val:,.2f}
        Average {num_col}: {mean_val:,.2f}
        Top Performing Segment ({cat_col}): {top_cat}
        Timeframe: {time_trend}
        """

        system_prompt = """You are the core analytical engine of 'DataPulse'. 
        Analyze the statistical summary and generate a strict, professional business report.
        CRITICAL RULES:
        - Do NOT use conversational filler, greetings, or reveal you are an AI.
        - Sound like an automated enterprise system outputting a terminal report.
        - Format your output EXACTLY with these three sections using HTML tags:
        
        <b>Executive Summary:</b> [1 concise sentence summarizing the overall performance]
        <br><br><b>Anomaly & Risk Detection:</b> [1 sentence identifying a potential outlier, dependency, or risk based on the data]
        <br><br><b>Actionable Forecast:</b> [1 sentence strategic recommendation for the user]"""

        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data_summary}
            ],
            temperature=0.2,
            max_tokens=350,
        )

        return _strip_think_tags(completion.choices[0].message.content)
    except Exception as e:
        return f"<b>System Diagnostics:</b><br>Analysis complete. Use visualizations to monitor metrics. (Error: {str(e)})"


# ═══════════════════════════════════════════════════════════════
# HELPER: Z-SCORE ANOMALY DETECTION
# ═══════════════════════════════════════════════════════════════
def detect_anomalies(df, numeric_cols, threshold=2.0):
    """Detect anomalies using Z-Score method across numeric columns."""
    anomaly_data = {}
    for col in numeric_cols:
        series = df[col].dropna()
        if len(series) < 3 or series.std() == 0:
            continue
        z_scores = np.abs((series - series.mean()) / series.std())
        anomaly_mask = z_scores > threshold
        if anomaly_mask.any():
            anomaly_indices = series[anomaly_mask].index.tolist()
            anomaly_data[col] = {
                "indices": anomaly_indices,
                "values": series[anomaly_mask].tolist(),
                "z_scores": z_scores[anomaly_mask].tolist(),
                "count": int(anomaly_mask.sum()),
                "mean": float(series.mean()),
                "std": float(series.std()),
            }
    return anomaly_data


# ═══════════════════════════════════════════════════════════════
# HELPER: CORRELATION MATRIX
# ═══════════════════════════════════════════════════════════════
def compute_correlation(df, numeric_cols):
    """Compute Pearson correlation matrix."""
    if len(numeric_cols) < 2:
        return None, []
    corr_df = df[numeric_cols].corr(method='pearson')
    corr_matrix = corr_df.values.tolist()
    # Round to 2 decimals
    corr_matrix = [[round(v, 2) for v in row] for row in corr_matrix]
    return corr_matrix, numeric_cols


# ═══════════════════════════════════════════════════════════════
# HELPER: LOCAL MATH SUMMARY FOR CORRELATION
# ═══════════════════════════════════════════════════════════════
def local_correlation_summary(corr_matrix, columns):
    """Generate a plain-English correlation summary without AI."""
    if not corr_matrix or len(columns) < 2:
        return "Insufficient numeric columns for correlation analysis."

    best_pos = {"val": -1, "pair": ("", "")}
    best_neg = {"val": 1, "pair": ("", "")}

    for i in range(len(columns)):
        for j in range(i + 1, len(columns)):
            val = corr_matrix[i][j]
            if val > best_pos["val"]:
                best_pos = {"val": val, "pair": (columns[i], columns[j])}
            if val < best_neg["val"]:
                best_neg = {"val": val, "pair": (columns[i], columns[j])}

    summary = f"<b>Strongest positive correlation:</b> {best_pos['pair'][0]} and {best_pos['pair'][1]} (r = {best_pos['val']:.2f}) — these metrics tend to increase together."
    if best_neg["val"] < 0:
        summary += f"<br><b>Strongest negative correlation:</b> {best_neg['pair'][0]} and {best_neg['pair'][1]} (r = {best_neg['val']:.2f}) — as one increases, the other tends to decrease."
    else:
        summary += "<br>No significant negative correlations detected in this dataset."

    return summary


# ═══════════════════════════════════════════════════════════════
# MAIN VIEW: FILE UPLOAD & DASHBOARD
# ═══════════════════════════════════════════════════════════════
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

            # ── AUTO-DETECT COLUMNS ──
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

            # ── EXTENDED KPI METRICS ──
            kpi_metrics = {
                "total": float(df[primary_num].sum()),
                "mean": float(df[primary_num].mean()),
                "median": float(df[primary_num].median()),
                "std": float(df[primary_num].std()) if len(df) > 1 else 0,
                "min": float(df[primary_num].min()),
                "max": float(df[primary_num].max()),
            }

            # ── AI INSIGHTS ──
            ai_insights_text = get_universal_insights(df, primary_num, primary_cat, date_col)

            # ── CHART DATA ──
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
                except Exception:
                    pass

            # ── Z-SCORE ANOMALY DETECTION ──
            anomaly_data = detect_anomalies(df, numeric_cols)

            # Anomaly scatter data for primary numeric column
            anomaly_scatter = {"normal_x": [], "normal_y": [], "anomaly_x": [], "anomaly_y": []}
            if primary_num in anomaly_data:
                anom_indices = set(anomaly_data[primary_num]["indices"])
                for idx, val in enumerate(df[primary_num].tolist()):
                    if idx in anom_indices:
                        anomaly_scatter["anomaly_x"].append(idx)
                        anomaly_scatter["anomaly_y"].append(val)
                    else:
                        anomaly_scatter["normal_x"].append(idx)
                        anomaly_scatter["normal_y"].append(val)
            else:
                for idx, val in enumerate(df[primary_num].tolist()):
                    anomaly_scatter["normal_x"].append(idx)
                    anomaly_scatter["normal_y"].append(val)

            # ── CORRELATION MATRIX ──
            corr_matrix, corr_columns = compute_correlation(df, numeric_cols)
            corr_summary_local = local_correlation_summary(corr_matrix, corr_columns) if corr_matrix else "Need at least 2 numeric columns for correlation analysis."

            # ── SERIALIZE DATAFRAME FOR CLIENT-SIDE (capped) ──
            df_for_client = df.head(MAX_ROWS_CLIENT)
            # Convert datetime columns to string for JSON serialization
            for col in df_for_client.columns:
                if pd.api.types.is_datetime64_any_dtype(df_for_client[col]):
                    df_for_client[col] = df_for_client[col].dt.strftime('%Y-%m-%d')
            data_json = df_for_client.to_json(orient='records')

            context = {
                'file_name': file_name,
                'total_rows': df.shape[0],
                'total_cols': df.shape[1],
                'data_html': df.head(10).to_html(classes="data-table", index=False),
                'bar_data': json.dumps(bar_data),
                'pie_data': json.dumps(pie_data),
                'trend_data': json.dumps(trend_data),
                'ai_insights': ai_insights_text,
                'kpi_metrics': json.dumps(kpi_metrics),
                'anomaly_data': json.dumps(anomaly_data),
                'anomaly_scatter': json.dumps(anomaly_scatter),
                'corr_matrix': json.dumps(corr_matrix) if corr_matrix else 'null',
                'corr_columns': json.dumps(corr_columns),
                'corr_summary_local': corr_summary_local,
                'data_json': data_json,
                'numeric_cols': json.dumps(numeric_cols),
                'categorical_cols': json.dumps(categorical_cols),
                'primary_num': primary_num,
                'primary_cat': primary_cat or '',
                'date_col': date_col or '',
            }
            return render(request, 'result.html', context)

        except Exception as e:
            return HttpResponse(f"❌ Error processing file: {str(e)}")

    return render(request, 'index.html')


# ═══════════════════════════════════════════════════════════════
# API: NATURAL LANGUAGE QUERY (ASK DATA)
# ═══════════════════════════════════════════════════════════════
@csrf_exempt
def api_query(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        query = body.get("query", "").strip().lower()
        data_records = body.get("data_json", [])
        ai_mode = body.get("ai_mode", "local")
        primary_num = body.get("primary_num", "")
        numeric_cols = body.get("numeric_cols", [])

        if not query or not data_records:
            return JsonResponse({"error": "Missing query or data"}, status=400)

        df = pd.DataFrame(data_records)

        # ── LOCAL MATH MODE: Regex-based query parsing ──
        result = _parse_local_query(df, query, primary_num, numeric_cols)

        if result:
            # If AI mode is enabled, also get a natural language explanation
            if ai_mode == "cloud" and client:
                try:
                    ai_explanation = _strip_think_tags(client.chat.completions.create(
                        model=GROQ_MODEL,
                        messages=[
                            {"role": "system", "content": "You are DataPulse analytics. Answer in 1 concise sentence. No filler. No greetings."},
                            {"role": "user", "content": f"The user asked: '{query}'. The computed answer is: {result['value']}. Explain this result briefly in context of the data."}
                        ],
                        temperature=0.2,
                        max_tokens=100,
                    ).choices[0].message.content)
                    result["ai_explanation"] = ai_explanation
                except Exception:
                    pass

            return JsonResponse(result)

        # ── CLOUD AI MODE: Send to Groq for complex queries ──
        if ai_mode == "cloud" and client:
            try:
                # Build a compact summary
                summary_lines = [f"Columns: {', '.join(df.columns.tolist())}"]
                for col in numeric_cols:
                    if col in df.columns:
                        summary_lines.append(f"{col}: sum={df[col].sum():.2f}, avg={df[col].mean():.2f}, min={df[col].min():.2f}, max={df[col].max():.2f}")

                completion = _strip_think_tags(client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": "You are DataPulse analytics. Answer the user's data question concisely in 1-2 sentences. Use the data summary. No filler."},
                        {"role": "user", "content": f"Data summary:\n{chr(10).join(summary_lines)}\n\nQuestion: {query}"}
                    ],
                    temperature=0.2,
                    max_tokens=150,
                ).choices[0].message.content)
                return JsonResponse({"type": "text", "label": "AI Answer", "value": completion})
            except Exception as e:
                return JsonResponse({"error": f"AI query failed: {str(e)}"}, status=500)

        return JsonResponse({"error": "Could not understand the query. Try: 'total sales', 'average revenue', 'max quantity'."}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


def _parse_local_query(df, query, primary_num, numeric_cols):
    """Parse natural language query using regex and return computed result."""

    # Determine target column
    target_col = primary_num
    for col in df.columns:
        if col.lower() in query:
            target_col = col
            break

    if target_col not in df.columns:
        return None

    # Ensure numeric
    try:
        series = pd.to_numeric(df[target_col], errors='coerce').dropna()
    except Exception:
        return None

    # Pattern matching
    if re.search(r'\b(total|sum|overall)\b', query):
        val = float(series.sum())
        return {"type": "kpi", "label": f"Total {target_col}", "value": f"{val:,.2f}", "raw_value": val}

    if re.search(r'\b(average|avg|mean)\b', query):
        val = float(series.mean())
        return {"type": "kpi", "label": f"Average {target_col}", "value": f"{val:,.2f}", "raw_value": val}

    if re.search(r'\b(max|maximum|highest|largest|top)\b', query):
        val = float(series.max())
        return {"type": "kpi", "label": f"Max {target_col}", "value": f"{val:,.2f}", "raw_value": val}

    if re.search(r'\b(min|minimum|lowest|smallest|bottom)\b', query):
        val = float(series.min())
        return {"type": "kpi", "label": f"Min {target_col}", "value": f"{val:,.2f}", "raw_value": val}

    if re.search(r'\b(median|mid|middle)\b', query):
        val = float(series.median())
        return {"type": "kpi", "label": f"Median {target_col}", "value": f"{val:,.2f}", "raw_value": val}

    if re.search(r'\b(count|how many|number of|rows)\b', query):
        val = int(len(series))
        return {"type": "kpi", "label": f"Count of {target_col}", "value": f"{val:,}", "raw_value": val}

    if re.search(r'\b(std|deviation|spread|variance)\b', query):
        val = float(series.std())
        return {"type": "kpi", "label": f"Std Dev of {target_col}", "value": f"{val:,.2f}", "raw_value": val}

    # Count where condition: "count where X > N"
    match = re.search(r'count\s+where\s+(\w+)\s*([><=!]+)\s*([\d.]+)', query)
    if match:
        col_name, op, threshold = match.group(1), match.group(2), float(match.group(3))
        for c in df.columns:
            if c.lower() == col_name.lower():
                try:
                    s = pd.to_numeric(df[c], errors='coerce').dropna()
                    if op == '>':
                        val = int((s > threshold).sum())
                    elif op == '<':
                        val = int((s < threshold).sum())
                    elif op in ('>=', '=>'):
                        val = int((s >= threshold).sum())
                    elif op in ('<=', '=<'):
                        val = int((s <= threshold).sum())
                    elif op == '==':
                        val = int((s == threshold).sum())
                    else:
                        val = 0
                    return {"type": "kpi", "label": f"Count where {c} {op} {threshold}", "value": f"{val:,}", "raw_value": val}
                except Exception:
                    pass

    return None


# ═══════════════════════════════════════════════════════════════
# API: WHAT-IF SCENARIO SIMULATOR
# ═══════════════════════════════════════════════════════════════
@csrf_exempt
def api_whatif(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        data_records = body.get("data_json", [])
        column = body.get("column", "")
        operation = body.get("operation", "increase_pct")
        value = float(body.get("value", 0))
        primary_cat = body.get("primary_cat", "")
        secondary_cat = body.get("secondary_cat", "")
        date_col = body.get("date_col", "")
        ai_mode = body.get("ai_mode", "local")

        if not data_records or not column:
            return JsonResponse({"error": "Missing data or column"}, status=400)

        df = pd.DataFrame(data_records)
        if column not in df.columns:
            return JsonResponse({"error": f"Column '{column}' not found"}, status=400)

        df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)

        # Original metrics
        original_metrics = {
            "total": float(df[column].sum()),
            "mean": float(df[column].mean()),
            "median": float(df[column].median()),
        }

        # Apply transformation
        if operation == "increase_pct":
            df[column] = df[column] * (1 + value / 100)
        elif operation == "decrease_pct":
            df[column] = df[column] * (1 - value / 100)
        elif operation == "multiply":
            df[column] = df[column] * value
        elif operation == "add":
            df[column] = df[column] + value
        elif operation == "set":
            df[column] = value

        # New metrics
        new_metrics = {
            "total": float(df[column].sum()),
            "mean": float(df[column].mean()),
            "median": float(df[column].median()),
        }

        # Rebuild chart data
        bar_data = {"labels": [], "values": [], "title": ""}
        if primary_cat and primary_cat in df.columns:
            bar_df = df.groupby(primary_cat)[column].sum().nlargest(10).reset_index()
            bar_data["labels"] = bar_df[primary_cat].astype(str).tolist()
            bar_data["values"] = bar_df[column].tolist()
            bar_data["title"] = f"Total {column} by {primary_cat} (What-If)"

        pie_data = {"labels": [], "values": [], "title": ""}
        cat_for_pie = secondary_cat if secondary_cat and secondary_cat in df.columns else (primary_cat if primary_cat and primary_cat in df.columns else "")
        if cat_for_pie:
            pie_df = df.groupby(cat_for_pie)[column].sum().nlargest(5).reset_index()
            pie_data["labels"] = pie_df[cat_for_pie].astype(str).tolist()
            pie_data["values"] = pie_df[column].tolist()
            pie_data["title"] = f"Top 5 {cat_for_pie} share in {column} (What-If)"

        trend_data = {"labels": [], "values": [], "title": ""}
        if date_col and date_col in df.columns:
            try:
                df[date_col] = pd.to_datetime(df[date_col])
                trend_df = df.groupby(df[date_col].dt.strftime('%Y-%m-%d'))[column].sum().reset_index()
                trend_data["labels"] = trend_df[date_col].tolist()
                trend_data["values"] = trend_df[column].tolist()
                trend_data["title"] = f"{column} Trend (What-If)"
            except Exception:
                pass

        response = {
            "original_metrics": original_metrics,
            "new_metrics": new_metrics,
            "bar_data": bar_data,
            "pie_data": pie_data,
            "trend_data": trend_data,
        }

        # AI forecast if enabled
        if ai_mode == "cloud" and client:
            try:
                change_desc = f"{operation.replace('_', ' ')} by {value}"
                forecast_prompt = f"The user simulated a what-if scenario: '{change_desc}' on column '{column}'. Original total: {original_metrics['total']:,.2f}, New total: {new_metrics['total']:,.2f}. Give a 1-sentence business impact forecast. No filler."
                completion = _strip_think_tags(client.chat.completions.create(
                    model=GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": "You are DataPulse analytics engine. Be concise and professional."},
                        {"role": "user", "content": forecast_prompt}
                    ],
                    temperature=0.3,
                    max_tokens=100,
                ).choices[0].message.content)
                response["ai_forecast"] = completion
            except Exception:
                response["ai_forecast"] = ""

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# ═══════════════════════════════════════════════════════════════
# API: CORRELATION SUMMARY (AI-POWERED)
# ═══════════════════════════════════════════════════════════════
@csrf_exempt
def api_correlation_summary(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        corr_matrix = body.get("corr_matrix", [])
        columns = body.get("columns", [])

        if not corr_matrix or not columns:
            return JsonResponse({"error": "Missing correlation data"}, status=400)

        if not client:
            summary = local_correlation_summary(corr_matrix, columns)
            return JsonResponse({"summary": summary, "mode": "local"})

        # Build a readable correlation description
        corr_desc_parts = []
        for i in range(len(columns)):
            for j in range(i + 1, len(columns)):
                corr_desc_parts.append(f"{columns[i]} vs {columns[j]}: r = {corr_matrix[i][j]}")

        prompt = f"""Correlation matrix results:
{chr(10).join(corr_desc_parts)}

Write exactly 2 sentences in plain English explaining the most important relationships. 
Be specific about column names and correlation strength. No filler. No greetings."""

        completion = _strip_think_tags(client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": "You are DataPulse analytics. Output only 2 sentences."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=150,
        ).choices[0].message.content)

        return JsonResponse({"summary": completion, "mode": "cloud"})

    except Exception as e:
        return JsonResponse({"summary": local_correlation_summary(
            body.get("corr_matrix", []), body.get("columns", [])
        ), "mode": "local_fallback", "error": str(e)})


# ═══════════════════════════════════════════════════════════════
# MATPLOTLIB CHART RENDERERS (Server-Side)
# ═══════════════════════════════════════════════════════════════

# ── GLOBAL MATPLOTLIB THEME ──
_MPL_BG = '#0f172a'
_MPL_CARD_BG = '#1e293b'
_MPL_TEXT = '#f1f5f9'
_MPL_TEXT_DIM = '#94a3b8'
_MPL_GRID = '#1e293b'
_MPL_ACCENT = '#a855f7'
_MPL_COLORS = ['#a855f7', '#38bdf8', '#ec4899', '#facc15', '#10b981',
               '#f97316', '#06b6d4', '#8b5cf6', '#f43f5e', '#14b8a6']


def _setup_mpl_style():
    """Configure Matplotlib for dark-themed premium chart rendering."""
    plt.rcParams.update({
        'figure.facecolor': _MPL_BG,
        'axes.facecolor': _MPL_CARD_BG,
        'axes.edgecolor': '#334155',
        'axes.labelcolor': _MPL_TEXT_DIM,
        'text.color': _MPL_TEXT,
        'xtick.color': _MPL_TEXT_DIM,
        'ytick.color': _MPL_TEXT_DIM,
        'grid.color': '#334155',
        'grid.alpha': 0.3,
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
    })


def _fig_to_image_reader(fig, dpi=180):
    """Convert a Matplotlib figure to a ReportLab-compatible Image (via BytesIO)."""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor(), edgecolor='none', pad_inches=0.3)
    plt.close(fig)
    buf.seek(0)
    return buf


def render_trend_chart_mpl(data, primary_num):
    """Render an area/line trend chart with Matplotlib."""
    _setup_mpl_style()
    fig, ax = plt.subplots(figsize=(10, 4))

    labels = data.get('labels', [])
    values = data.get('values', [])
    title = data.get('title', f'{primary_num} Trend')

    if not labels or not values:
        plt.close(fig)
        return None

    x = range(len(labels))
    ax.fill_between(x, values, alpha=0.25, color=_MPL_ACCENT)
    ax.plot(x, values, color=_MPL_ACCENT, linewidth=2.5, marker='o',
            markersize=4, markerfacecolor=_MPL_ACCENT, markeredgecolor='white',
            markeredgewidth=0.8)

    # X-axis labels (show max 15 to avoid crowding)
    step = max(1, len(labels) // 15)
    tick_positions = list(range(0, len(labels), step))
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([labels[i] for i in tick_positions], rotation=45,
                       ha='right', fontsize=8)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:,.0f}'))
    ax.set_title(title, pad=12, color=_MPL_TEXT)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    return _fig_to_image_reader(fig)


def render_bar_chart_mpl(data):
    """Render a vertical bar chart with Matplotlib."""
    _setup_mpl_style()
    fig, ax = plt.subplots(figsize=(10, 4.5))

    labels = data.get('labels', [])
    values = data.get('values', [])
    title = data.get('title', 'Bar Chart')

    if not labels or not values:
        plt.close(fig)
        return None

    bar_colors = [_MPL_COLORS[i % len(_MPL_COLORS)] for i in range(len(labels))]
    bars = ax.bar(labels, values, color=bar_colors, width=0.6, edgecolor='none',
                  zorder=3, alpha=0.9)

    # Add value labels on top
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                f'{val:,.0f}', ha='center', va='bottom', fontsize=8,
                color=_MPL_TEXT_DIM, fontweight='bold')

    ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=9)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f'{v:,.0f}'))
    ax.set_title(title, pad=12, color=_MPL_TEXT)
    ax.grid(True, axis='y', linestyle='--', alpha=0.3, zorder=0)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    return _fig_to_image_reader(fig)


def render_donut_chart_mpl(data):
    """Render a donut/pie chart with Matplotlib."""
    _setup_mpl_style()
    fig, ax = plt.subplots(figsize=(6, 5))

    labels = data.get('labels', [])
    values = data.get('values', [])
    title = data.get('title', 'Distribution')

    if not labels or not values:
        plt.close(fig)
        return None

    chart_colors = [_MPL_COLORS[i % len(_MPL_COLORS)] for i in range(len(labels))]
    wedges, texts, autotexts = ax.pie(
        values, labels=None, autopct='%1.1f%%', pctdistance=0.78,
        colors=chart_colors, startangle=90,
        wedgeprops=dict(width=0.38, edgecolor=_MPL_BG, linewidth=2.5))

    for t in autotexts:
        t.set_color('white')
        t.set_fontsize(9)
        t.set_fontweight('bold')

    # Center text
    total = sum(values)
    ax.text(0, 0.06, f'{total:,.0f}', ha='center', va='center',
            fontsize=20, fontweight='bold', color=_MPL_TEXT)
    ax.text(0, -0.12, 'Total', ha='center', va='center',
            fontsize=10, color=_MPL_TEXT_DIM)

    # Legend
    ax.legend(wedges, labels, loc='lower center', bbox_to_anchor=(0.5, -0.15),
              ncol=min(3, len(labels)), fontsize=9, frameon=False,
              labelcolor=_MPL_TEXT_DIM)

    ax.set_title(title, pad=16, color=_MPL_TEXT)
    fig.tight_layout()
    return _fig_to_image_reader(fig)


def render_anomaly_scatter_mpl(scatter_data, primary_num, anomaly_data):
    """Render an anomaly scatter plot with Matplotlib."""
    _setup_mpl_style()
    fig, ax = plt.subplots(figsize=(10, 4.5))

    normal_x = scatter_data.get('normal_x', [])
    normal_y = scatter_data.get('normal_y', [])
    anomaly_x = scatter_data.get('anomaly_x', [])
    anomaly_y = scatter_data.get('anomaly_y', [])

    if not normal_x and not anomaly_x:
        plt.close(fig)
        return None

    if normal_x:
        ax.scatter(normal_x, normal_y, c='#38bdf8', s=30, alpha=0.6,
                   label='Normal', zorder=3, edgecolors='none')
    if anomaly_x:
        ax.scatter(anomaly_x, anomaly_y, c='#ef4444', s=70, alpha=0.9,
                   label=f'Anomaly (Z > 2.0)', zorder=4, edgecolors='white',
                   linewidth=1.2, marker='D')

    # Mean line
    prim_anom = anomaly_data.get(primary_num, {})
    if prim_anom and 'mean' in prim_anom:
        ax.axhline(y=prim_anom['mean'], color='#facc15', linestyle='--',
                   linewidth=1.2, alpha=0.7, label=f'Mean: {prim_anom["mean"]:,.1f}')

    ax.set_xlabel('Data Point Index', fontsize=10)
    ax.set_ylabel(primary_num, fontsize=10)
    ax.set_title(f'{primary_num} — Anomaly Detection (Z-Score > 2.0)', pad=12, color=_MPL_TEXT)
    ax.legend(fontsize=9, frameon=False, labelcolor=_MPL_TEXT_DIM, loc='upper right')
    ax.grid(True, linestyle='--', alpha=0.2)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    fig.tight_layout()
    return _fig_to_image_reader(fig)


def render_heatmap_mpl(corr_matrix, corr_columns):
    """Render a correlation heatmap with Matplotlib."""
    _setup_mpl_style()
    n = len(corr_columns)
    if n < 2 or not corr_matrix:
        return None

    fig, ax = plt.subplots(figsize=(max(6, n * 1.1), max(5, n * 0.9)))

    data_arr = np.array(corr_matrix)
    im = ax.imshow(data_arr, cmap='RdYlBu_r', aspect='auto', vmin=-1, vmax=1)

    # Annotations
    for i in range(n):
        for j in range(n):
            val = data_arr[i, j]
            text_color = 'white' if abs(val) > 0.5 else _MPL_TEXT
            ax.text(j, i, f'{val:.2f}', ha='center', va='center',
                    fontsize=max(8, 12 - n // 2), color=text_color, fontweight='bold')

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(corr_columns, rotation=45, ha='right', fontsize=9)
    ax.set_yticklabels(corr_columns, fontsize=9)
    ax.set_title('Pearson Correlation Matrix', pad=16, color=_MPL_TEXT)

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.ax.tick_params(colors=_MPL_TEXT_DIM, labelsize=8)
    cbar.outline.set_edgecolor('#334155')

    fig.tight_layout()
    return _fig_to_image_reader(fig)


# ═══════════════════════════════════════════════════════════════
# REPORTLAB PDF BUILDER
# ═══════════════════════════════════════════════════════════════

# ── COLOR PALETTE ──
_PDF_BG = HexColor('#0f172a')
_PDF_CARD_BG = HexColor('#1e293b')
_PDF_ACCENT = HexColor('#a855f7')
_PDF_ACCENT_LIGHT = HexColor('#c084fc')
_PDF_CYAN = HexColor('#38bdf8')
_PDF_TEXT = HexColor('#f1f5f9')
_PDF_TEXT_DIM = HexColor('#94a3b8')
_PDF_TEXT_MUTED = HexColor('#64748b')
_PDF_BORDER = HexColor('#334155')
_PDF_RED = HexColor('#ef4444')
_PDF_GREEN = HexColor('#10b981')


def _pdf_styles():
    """Create a custom style sheet for the DataPulse PDF report."""
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'DP_Title', parent=styles['Title'],
        fontSize=28, leading=34, textColor=_PDF_TEXT,
        alignment=TA_CENTER, spaceAfter=4, fontName='Helvetica-Bold',
    ))
    styles.add(ParagraphStyle(
        'DP_Subtitle', parent=styles['Normal'],
        fontSize=11, leading=14, textColor=_PDF_TEXT_DIM,
        alignment=TA_CENTER, spaceAfter=20,
    ))
    styles.add(ParagraphStyle(
        'DP_SectionTitle', parent=styles['Heading2'],
        fontSize=16, leading=20, textColor=_PDF_ACCENT_LIGHT,
        spaceBefore=16, spaceAfter=10, fontName='Helvetica-Bold',
    ))
    styles.add(ParagraphStyle(
        'DP_Body', parent=styles['Normal'],
        fontSize=10, leading=15, textColor=_PDF_TEXT_DIM,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        'DP_BodyLight', parent=styles['Normal'],
        fontSize=9.5, leading=14, textColor=_PDF_TEXT_MUTED,
        spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        'DP_KPI_Value', parent=styles['Normal'],
        fontSize=22, leading=26, textColor=_PDF_TEXT,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
    ))
    styles.add(ParagraphStyle(
        'DP_KPI_Label', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=_PDF_TEXT_MUTED,
        alignment=TA_CENTER, spaceAfter=0,
    ))
    styles.add(ParagraphStyle(
        'DP_Footer', parent=styles['Normal'],
        fontSize=8, leading=10, textColor=_PDF_TEXT_MUTED,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'DP_InsightBlock', parent=styles['Normal'],
        fontSize=10, leading=16, textColor=_PDF_TEXT_DIM,
        leftIndent=14, borderPadding=12, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        'DP_TableHeader', parent=styles['Normal'],
        fontSize=9, leading=11, textColor=_PDF_TEXT,
        alignment=TA_CENTER, fontName='Helvetica-Bold',
    ))
    styles.add(ParagraphStyle(
        'DP_TableCell', parent=styles['Normal'],
        fontSize=8.5, leading=11, textColor=_PDF_TEXT_DIM,
        alignment=TA_CENTER,
    ))

    return styles


def _section_divider():
    """Return a styled horizontal rule element."""
    return HRFlowable(
        width="100%", thickness=1.2, lineCap='round',
        color=HexColor('#334155'), spaceBefore=6, spaceAfter=14,
    )


def _add_page_background(canvas, doc):
    """Draw the dark background and footer on each page."""
    canvas.saveState()
    # Full page dark background
    canvas.setFillColor(_PDF_BG)
    canvas.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)

    # Subtle accent line at top
    canvas.setStrokeColor(_PDF_ACCENT)
    canvas.setLineWidth(2.5)
    canvas.line(0, doc.pagesize[1] - 2, doc.pagesize[0], doc.pagesize[1] - 2)

    # Footer
    canvas.setFont('Helvetica', 7.5)
    canvas.setFillColor(_PDF_TEXT_MUTED)
    footer_text = f"DataPulse Analytics Report  •  Page {doc.page}"
    canvas.drawCentredString(doc.pagesize[0] / 2, 18 * mm, footer_text)

    # Footer accent line
    canvas.setStrokeColor(HexColor('#1e293b'))
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 22 * mm,
                doc.pagesize[0] - doc.rightMargin, 22 * mm)

    canvas.restoreState()


def _build_kpi_table(kpi_metrics, styles, page_width):
    """Build a 3x2 grid of KPI cards as a ReportLab Table."""
    def _kpi_cell(label, value):
        return [
            Paragraph(f'{value}', styles['DP_KPI_Value']),
            Paragraph(label.upper(), styles['DP_KPI_Label']),
        ]

    m = kpi_metrics
    cell_data = [
        [
            _kpi_cell('Total Sum', f'{m["total"]:,.2f}'),
            _kpi_cell('Average', f'{m["mean"]:,.2f}'),
            _kpi_cell('Median', f'{m["median"]:,.2f}'),
        ],
        [
            _kpi_cell('Std Deviation', f'{m["std"]:,.2f}'),
            _kpi_cell('Minimum', f'{m["min"]:,.2f}'),
            _kpi_cell('Maximum', f'{m["max"]:,.2f}'),
        ],
    ]

    # Flatten cells: each cell is a list of [value_para, label_para] → wrap in a mini table
    def _cell_table(cell_content):
        t = Table([[cell_content[0]], [cell_content[1]]],
                  colWidths=[page_width / 3 - 20])
        t.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        return t

    table_data = [
        [_cell_table(cell_data[0][0]), _cell_table(cell_data[0][1]), _cell_table(cell_data[0][2])],
        [_cell_table(cell_data[1][0]), _cell_table(cell_data[1][1]), _cell_table(cell_data[1][2])],
    ]

    col_w = page_width / 3
    kpi_table = Table(table_data, colWidths=[col_w, col_w, col_w])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), _PDF_CARD_BG),
        ('BOX', (0, 0), (-1, -1), 0.5, _PDF_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, _PDF_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 14),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 14),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))

    return kpi_table


def _build_data_table(data_records, styles, page_width, max_rows=20):
    """Build a styled data table from the first N records."""
    if not data_records:
        return None

    df = pd.DataFrame(data_records[:max_rows])
    columns = list(df.columns)

    # Limit columns to avoid overflow
    max_cols = 8
    if len(columns) > max_cols:
        columns = columns[:max_cols]
        df = df[columns]

    col_w = page_width / len(columns)
    col_widths = [col_w] * len(columns)

    # Header row
    header = [Paragraph(str(c), styles['DP_TableHeader']) for c in columns]
    table_data = [header]

    # Data rows
    for _, row in df.iterrows():
        row_cells = []
        for c in columns:
            val = row[c]
            if isinstance(val, (int, float)):
                text = f'{val:,.2f}' if isinstance(val, float) else f'{val:,}'
            else:
                text = str(val)[:25]  # Truncate long strings
            row_cells.append(Paragraph(text, styles['DP_TableCell']))
        table_data.append(row_cells)

    tbl = Table(table_data, colWidths=col_widths, repeatRows=1)

    # Style
    style_cmds = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2d1b69')),  # Header purple
        ('TEXTCOLOR', (0, 0), (-1, 0), _PDF_TEXT),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 7),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 7),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 0.5, _PDF_BORDER),
        ('LINEBELOW', (0, 0), (-1, 0), 1, _PDF_ACCENT),
        ('INNERGRID', (0, 1), (-1, -1), 0.3, HexColor('#1e293b')),
    ]

    # Alternating row colors
    for i in range(1, len(table_data)):
        bg = _PDF_CARD_BG if i % 2 == 0 else HexColor('#162032')
        style_cmds.append(('BACKGROUND', (0, i), (-1, i), bg))

    tbl.setStyle(TableStyle(style_cmds))
    return tbl


def _build_anomaly_stats_table(anomaly_data, primary_num, scatter_data, styles, page_width):
    """Build anomaly summary statistics as a card-style table."""
    prim_anom = anomaly_data.get(primary_num, {})
    total_anomalies = prim_anom.get('count', 0)
    total_points = len(scatter_data.get('normal_x', [])) + len(scatter_data.get('anomaly_x', []))
    anomaly_pct = (total_anomalies / total_points * 100) if total_points > 0 else 0
    mean_val = prim_anom.get('mean', 0)

    cells = [
        [
            Paragraph(f'<font color="#ef4444" size="18"><b>{total_anomalies}</b></font>', styles['DP_Body']),
            Paragraph(f'<font color="#38bdf8" size="18"><b>{total_points:,}</b></font>', styles['DP_Body']),
            Paragraph(f'<font color="{"#ef4444" if total_anomalies > 0 else "#10b981"}" size="18"><b>{anomaly_pct:.1f}%</b></font>', styles['DP_Body']),
            Paragraph(f'<font color="#38bdf8" size="18"><b>{mean_val:,.1f}</b></font>', styles['DP_Body']),
        ],
        [
            Paragraph('<font size="8" color="#64748b">ANOMALIES FOUND</font>', styles['DP_Body']),
            Paragraph('<font size="8" color="#64748b">TOTAL DATA POINTS</font>', styles['DP_Body']),
            Paragraph('<font size="8" color="#64748b">ANOMALY RATE</font>', styles['DP_Body']),
            Paragraph(f'<font size="8" color="#64748b">MEAN ({primary_num[:15]})</font>', styles['DP_Body']),
        ],
    ]

    col_w = page_width / 4
    tbl = Table(cells, colWidths=[col_w] * 4)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), _PDF_CARD_BG),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 1), (-1, 1), 12),
        ('BOX', (0, 0), (-1, -1), 0.5, _PDF_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.3, _PDF_BORDER),
        ('ROUNDEDCORNERS', [6, 6, 6, 6]),
    ]))
    return tbl


# ═══════════════════════════════════════════════════════════════
# API: PDF EXPORT ENDPOINT
# ═══════════════════════════════════════════════════════════════

@csrf_exempt
def api_export_pdf(request):
    """Generate a premium PDF report with real Matplotlib chart images."""
    if request.method != 'POST':
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        body = json.loads(request.body)
        selections = body.get('selections', {})
        file_name = body.get('file_name', 'Unknown')
        kpi_metrics = body.get('kpi_metrics', {})
        bar_data = body.get('bar_data', {})
        pie_data = body.get('pie_data', {})
        trend_data = body.get('trend_data', {})
        anomaly_data = body.get('anomaly_data', {})
        anomaly_scatter = body.get('anomaly_scatter', {})
        corr_matrix = body.get('corr_matrix', None)
        corr_columns = body.get('corr_columns', [])
        corr_summary = body.get('corr_summary', '')
        ai_insights = body.get('ai_insights', '')
        data_records = body.get('data_json', [])
        primary_num = body.get('primary_num', '')
        total_rows = body.get('total_rows', 0)
        total_cols = body.get('total_cols', 0)

        # ── Setup PDF document ──
        pdf_buffer = io.BytesIO()
        page_size = landscape(A4)
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=page_size,
            leftMargin=28 * mm,
            rightMargin=28 * mm,
            topMargin=20 * mm,
            bottomMargin=28 * mm,
        )

        styles = _pdf_styles()
        elements = []
        usable_width = page_size[0] - doc.leftMargin - doc.rightMargin

        from datetime import datetime
        report_date = datetime.now().strftime('%B %d, %Y at %I:%M %p')
        iso_date = datetime.now().strftime('%Y-%m-%d')

        # ═══════════════════════════════════════════
        # COVER / HEADER
        # ═══════════════════════════════════════════
        elements.append(Spacer(1, 30))
        elements.append(Paragraph(
            'Data<font color="#a855f7">Pulse</font> Analytics Report',
            styles['DP_Title']
        ))
        elements.append(Paragraph(
            f'Generated on {report_date}  •  File: {file_name}  •  '
            f'{total_rows:,} records × {total_cols} columns',
            styles['DP_Subtitle']
        ))
        elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # EXECUTIVE AI SUMMARY
        # ═══════════════════════════════════════════
        if selections.get('summary') and ai_insights:
            elements.append(Paragraph(
                '✦ Executive AI Summary',
                styles['DP_SectionTitle']
            ))

            # Strip HTML tags for clean PDF text, but preserve line breaks
            import html as html_module
            clean_text = ai_insights
            # Convert <br> and <br/> to newlines
            clean_text = re.sub(r'<br\s*/?>', '<br/>', clean_text)
            # Convert <b> tags to ReportLab bold
            clean_text = clean_text.replace('<b>', '<b>').replace('</b>', '</b>')
            # Remove any other HTML tags
            clean_text = re.sub(r'<(?!b>|/b>|br/)([^>]+)>', '', clean_text)

            elements.append(Paragraph(clean_text, styles['DP_InsightBlock']))
            elements.append(Spacer(1, 8))
            elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # KPI METRICS
        # ═══════════════════════════════════════════
        if selections.get('kpi') and kpi_metrics:
            elements.append(Paragraph(
                '📊 Key Performance Indicators',
                styles['DP_SectionTitle']
            ))
            elements.append(Spacer(1, 4))
            elements.append(_build_kpi_table(kpi_metrics, styles, usable_width))
            elements.append(Spacer(1, 8))
            elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # TREND CHART
        # ═══════════════════════════════════════════
        if selections.get('trend') and trend_data.get('labels'):
            elements.append(Paragraph(
                '📈 Trend Analysis',
                styles['DP_SectionTitle']
            ))
            chart_buf = render_trend_chart_mpl(trend_data, primary_num)
            if chart_buf:
                img = Image(chart_buf, width=usable_width, height=usable_width * 0.38)
                elements.append(img)
            elements.append(Spacer(1, 8))
            elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # BAR CHART
        # ═══════════════════════════════════════════
        if selections.get('bar') and bar_data.get('labels'):
            elements.append(Paragraph(
                '📊 Category Breakdown',
                styles['DP_SectionTitle']
            ))
            chart_buf = render_bar_chart_mpl(bar_data)
            if chart_buf:
                img = Image(chart_buf, width=usable_width, height=usable_width * 0.40)
                elements.append(img)
            elements.append(Spacer(1, 8))
            elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # PIE / DONUT CHART
        # ═══════════════════════════════════════════
        if selections.get('pie') and pie_data.get('labels'):
            elements.append(Paragraph(
                '🍩 Distribution Analysis',
                styles['DP_SectionTitle']
            ))
            chart_buf = render_donut_chart_mpl(pie_data)
            if chart_buf:
                img = Image(chart_buf, width=usable_width * 0.6, height=usable_width * 0.48)
                img.hAlign = 'CENTER'
                elements.append(img)
            elements.append(Spacer(1, 8))
            elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # ANOMALY DETECTION
        # ═══════════════════════════════════════════
        if selections.get('anomaly'):
            elements.append(Paragraph(
                '⚠ Anomaly Detection Report',
                styles['DP_SectionTitle']
            ))
            # Stats table
            stats_table = _build_anomaly_stats_table(
                anomaly_data, primary_num, anomaly_scatter, styles, usable_width
            )
            elements.append(stats_table)
            elements.append(Spacer(1, 10))

            # Scatter chart
            chart_buf = render_anomaly_scatter_mpl(anomaly_scatter, primary_num, anomaly_data)
            if chart_buf:
                img = Image(chart_buf, width=usable_width, height=usable_width * 0.40)
                elements.append(img)
            elements.append(Spacer(1, 8))
            elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # CORRELATION ANALYSIS
        # ═══════════════════════════════════════════
        if selections.get('correlation') and corr_matrix and len(corr_columns) >= 2:
            elements.append(Paragraph(
                '🔗 Correlation Analysis',
                styles['DP_SectionTitle']
            ))

            chart_buf = render_heatmap_mpl(corr_matrix, corr_columns)
            if chart_buf:
                hm_size = min(usable_width * 0.75, usable_width)
                img = Image(chart_buf, width=hm_size, height=hm_size * 0.78)
                img.hAlign = 'CENTER'
                elements.append(img)

            if corr_summary:
                elements.append(Spacer(1, 8))
                # Clean HTML for ReportLab
                clean_summary = corr_summary.replace('<b>', '<b>').replace('</b>', '</b>')
                clean_summary = re.sub(r'<br\s*/?>', '<br/>', clean_summary)
                clean_summary = re.sub(r'<(?!b>|/b>|br/)([^>]+)>', '', clean_summary)
                elements.append(Paragraph(clean_summary, styles['DP_InsightBlock']))

            elements.append(Spacer(1, 8))
            elements.append(_section_divider())

        # ═══════════════════════════════════════════
        # DATA TABLE
        # ═══════════════════════════════════════════
        if selections.get('table') and data_records:
            elements.append(Paragraph(
                '📋 Raw Data Preview',
                styles['DP_SectionTitle']
            ))
            elements.append(Paragraph(
                f'Showing first {min(20, len(data_records))} of {total_rows:,} records',
                styles['DP_BodyLight']
            ))
            elements.append(Spacer(1, 6))
            data_table = _build_data_table(data_records, styles, usable_width)
            if data_table:
                elements.append(data_table)
            elements.append(Spacer(1, 8))

        # ═══════════════════════════════════════════
        # CLOSING FOOTER
        # ═══════════════════════════════════════════
        elements.append(Spacer(1, 20))
        elements.append(HRFlowable(
            width="60%", thickness=0.8, lineCap='round',
            color=_PDF_BORDER, spaceBefore=10, spaceAfter=10,
        ))
        elements.append(Paragraph(
            f'This report was generated by <font color="#a855f7"><b>DataPulse</b></font> Analytics Engine  •  {report_date}',
            styles['DP_Footer']
        ))
        elements.append(Paragraph(
            'Automated data analysis with AI-powered insights',
            styles['DP_Footer']
        ))

        # ── Build PDF ──
        doc.build(elements, onFirstPage=_add_page_background,
                  onLaterPages=_add_page_background)

        pdf_buffer.seek(0)

        response = HttpResponse(pdf_buffer.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="DataPulse_Report_{iso_date}.pdf"'
        return response

    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({"error": f"PDF generation failed: {str(e)}"}, status=500)