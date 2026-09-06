import pandas as pd
import numpy as np
import json
import re
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from groq import Groq

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