# 📊 DataPulse Analytics

### *AI-Powered Data Analysis, Visualization & Decision Intelligence Platform*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-Web%20Dashboard-092E20?style=for-the-badge&logo=django&logoColor=white" />
</p>


<p align="center">
  <img src="https://img.shields.io/badge/AI-Powered-00F3FF?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Groq-Cloud%20AI-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Privacy-Local%20Math%20Mode-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-Active%20Development-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

---

# 🚀 What is DataPulse?

**DataPulse Analytics** is a Python-based intelligent data analytics platform designed to transform raw datasets into meaningful statistics, interactive visualizations, AI-generated insights, anomaly detection results, scenario simulations, and professional analytical reports.

DataPulse combines:

* 🐍 Python
* 🐼 Pandas
* 🔢 NumPy
* 📊 Matplotlib
* 🌐 Django
* 🤖 AI Integration
* ⚡ Groq-powered Cloud AI
* 🔐 Privacy-focused Local Analytics

into a single modular analytics platform.

Instead of treating data analysis as simply creating charts, DataPulse follows a complete intelligence pipeline:

> **Upload → Clean → Analyze → Visualize → Simulate → Detect → Query → Understand → Decide → Report**

---

# ✨ Why DataPulse?

Modern datasets often contain more information than traditional charts can easily explain.

DataPulse is designed to answer questions such as:

> **What happened?**

> **Why did it happen?**

> **What unusual patterns exist?**

> **What happens if a value changes?**

> **Which columns are correlated?**

> **Can I ask questions about my dataset using natural language?**

> **What actionable insights can AI generate from my data?**

> **Can I analyze sensitive data without sending it to an external API?**

DataPulse brings these capabilities together inside one dashboard.

---

# 🧠 Core Features

## 📂 1. Smart Dataset Upload

Upload datasets directly from the dashboard without modifying Python source code.

### Supported Formats

* 📄 CSV
* 📝 TXT
* 📊 XLSX / Excel

The platform automatically loads the dataset and prepares it for analysis.

---

# 🧹 2. Automated Data Cleaning

DataPulse includes an automated preprocessing pipeline for preparing raw datasets.

### Cleaning Capabilities

* Duplicate detection
* Duplicate removal
* Missing-value handling
* Date conversion
* Data normalization
* Numerical data processing
* Column type detection
* Clean dataset generation
* Processed dataset export

### Processing Flow

```text
Raw Dataset
     │
     ▼
Data Loader
     │
     ▼
Data Type Detection
     │
     ▼
Missing Value Handling
     │
     ▼
Duplicate Removal
     │
     ▼
Normalization
     │
     ▼
Clean Dataset
```

---

# 📊 3. Statistical Analysis Engine

DataPulse automatically extracts important statistical information from the dataset.

### Analytics Include

* Total
* Average
* Minimum
* Maximum
* Count
* Sum
* Median
* Standard deviation
* Numerical column statistics
* Category-level statistics
* Product-level statistics
* KPI calculations

For sales-oriented datasets, analytics can include:

* 💰 Total Revenue
* 📦 Total Units Sold
* 📈 Average Sale Value
* ⬆️ Highest Sale
* ⬇️ Lowest Sale
* 🏆 Top Category
* 🥇 Best-Selling Product
* 📊 Profit Analysis

---

# 📈 4. Matplotlib Visualization Engine

DataPulse converts analytical results into meaningful visualizations using Matplotlib.

### Supported Visualizations

* 📊 Bar Chart
* 📈 Line Chart
* 🥧 Pie Chart
* 🔵 Scatter Plot
* 📊 Histogram
* 📉 Trend Analysis
* 🔥 Correlation Heatmap
* 📌 Category Comparison
* 📈 Time-Series Analysis


### Example Visualizations

#### Category Sales

Compares performance across different categories.

#### Daily Sales Trend

Shows how a metric changes over time.

#### Product Distribution

Highlights the contribution of top-performing products.

---

# 🔮 5. What-If Scenario Simulator

One of the advanced decision-support features of DataPulse.

The **What-If Scenario Simulator** allows users to modify a target column temporarily and observe how the analytical results change.

### Scenario Configuration

```text
Target Column
      ↓
Operation
      ↓
Value
      ↓
Simulate
      ↓
Compare Results
```

### Available Operations

Depending on the dataset and implementation:

* Increase
* Decrease
* Add
* Subtract
* Multiply
* Divide
* Percentage Change

### Example

Suppose the dataset contains:

```text
Sales
100000
150000
200000
```

A user can configure:

```text
Target Column : Sales
Operation     : Increase
Value         : 10%
```

DataPulse can simulate the modified scenario and compare it against the original dataset.

### Scenario Analysis

```text
Original Data
      │
      ├──────────────┐
      │              │
      ▼              ▼
Current Metrics   What-If Scenario
      │              │
      └──────┬───────┘
             ▼
      Comparison
             │
             ▼
      Decision Insight
```

This feature helps users understand **potential outcomes before making decisions**.

---

# 🚨 6. Smart Anomaly Detection

DataPulse automatically searches for unusual values and unexpected patterns.

The Smart Anomaly Detection engine can identify:

* Extreme values
* Unusual numerical observations
* Unexpected spikes
* Unexpected drops
* Statistical outliers
* Abnormal patterns

### Conceptual Flow

```text
Dataset
   │
   ▼
Numerical Analysis
   │
   ▼
Pattern Detection
   │
   ▼
Outlier Identification
   │
   ▼
Anomaly Score
   │
   ▼
Visual Highlighting
```

Anomalies can then be presented through tables, charts, and analytical explanations.

---

# 🔥 7. Hidden Correlation Heatmap

DataPulse can analyze relationships between numerical columns to reveal hidden patterns.

The correlation engine helps identify:

* Positive relationships
* Negative relationships
* Weak relationships
* Strong relationships
* Potentially interesting variable pairs

### Example

```text
              Sales   Profit   Units   Price
Sales          1.00    0.86     0.72    0.61
Profit         0.86    1.00     0.65    0.74
Units          0.72    0.65     1.00    0.21
Price          0.61    0.74     0.21    1.00
```

The heatmap provides a visual way to explore these relationships.

> **Note:** Correlation indicates association, not causation.

---

# 💬 8. Natural Language Query Engine

DataPulse allows users to interact with their dataset using simple natural-language questions.

Instead of manually writing Pandas code, users can ask questions such as:

```text
What is the total sales?

What is the average profit?

What is the minimum sales?

What is the maximum sales?

How many records are there?

What is the total units sold?
```

### Query Pipeline

```text
User Question
      │
      ▼
Query Understanding
      │
      ▼
Column Detection
      │
      ▼
Operation Detection
      │
      ▼
Data Calculation
      │
      ▼
Human-Friendly Answer
```

This makes DataPulse easier to use for users who may not know Python or Pandas.

---

# 🤖 9. AI Insights Engine

The **AI Insights Engine** reads analytical results and converts them into understandable insights.

Instead of only displaying:

```text
Average Sales: ₹84,500
```

DataPulse can provide a higher-level interpretation such as:

```text
Sales performance is relatively strong, but the dataset
contains noticeable variation between individual records.
Further investigation of category and regional performance
may reveal the source of this variation.
```

### AI Insight Categories

* 📊 Performance Insights
* 📈 Trend Insights
* 🚨 Anomaly Insights
* 🔗 Correlation Insights
* 💡 Recommendations
* ⚠️ Risk Indicators
* 🎯 Decision Suggestions
* 📌 KPI Interpretation

---

# 🔐 10. Privacy & AI Mode

DataPulse provides a privacy-focused AI configuration that allows users to control how analytical intelligence is generated.

## 🛡️ Local Math Mode

> **Data stays private.**

In Local Math Mode:

* No external AI API calls are required
* Statistical calculations happen locally
* Dataset processing remains on the local machine
* Core analytics work without cloud AI

```text
Dataset
   │
   ▼
Local Python Engine
   │
   ├── Pandas
   ├── NumPy
   └── Statistical Analysis
   │
   ▼
Local Insights
```

This mode is ideal for sensitive datasets.

---

## ☁️ Cloud AI Mode

Cloud AI Mode enables AI-powered insights using a Groq-powered integration.

```text
Dataset
   │
   ▼
Analytics Engine
   │
   ▼
AI Insight Preparation
   │
   ▼
Groq AI
   │
   ▼
AI Generated Insights
```

Users can switch between:

```text
🔐 Local Math Mode
        ↕
☁️ Cloud AI Mode
```

depending on their privacy and intelligence requirements.

> **Privacy Note:** Users should review their deployment and API configuration before sending sensitive data to any external AI service.

---

# 🚦 11. KPI Threshold Alerts

DataPulse includes configurable KPI threshold monitoring.

Users can define:

```text
Minimum Threshold
Maximum Threshold
```

for a primary metric.

### Example

```text
KPI Metric       : Sales
Min Threshold   : 50,000
Max Threshold   : 200,000
```

If the metric violates the configured limits, DataPulse can visually highlight the KPI.

### Alert Logic

```text
             KPI Value
                 │
       ┌─────────┴─────────┐
       ▼                   ▼
 Below Minimum        Above Maximum
       │                   │
       ▼                   ▼
  ⚠️ Alert             🚨 Alert
```

The dashboard can use visual/neon alert states to make threshold violations immediately noticeable.

---

# 📄 12. Modular PDF Export

DataPulse provides a modular report-generation system.

Users can choose exactly what should appear in the final PDF report.

### Export Components

Possible report sections include:

* 📊 KPI Summary
* 📈 Charts
* 📋 Dataset Statistics
* 🚨 Anomaly Detection Results
* 🔥 Correlation Analysis
* 🔮 What-If Scenario Results
* 🤖 AI Insights
* 💡 Recommendations
* 📌 Key Findings

### Export Flow

```text
Dashboard
    │
    ▼
Select Report Sections
    │
    ▼
Generate Report
    │
    ▼
Format & Layout
    │
    ▼
Print-Ready PDF
```

This allows users to create customized analytical reports instead of exporting unnecessary information.

---

# 🌐 13. Django Analytics Dashboard

DataPulse includes a browser-based dashboard powered by Django.

### Dashboard Capabilities

* Dataset upload
* Dataset preview
* Row and column statistics
* Dynamic visualizations
* KPI cards
* Category analytics
* Product analytics
* Trend analysis
* What-If Simulator
* Anomaly Detection
* Correlation Heatmap
* Natural Language Query
* AI Insights
* KPI Threshold Settings
* Privacy & AI Mode
* PDF Export

---

# 📊 Dashboard Intelligence

The dashboard is designed around an analytics-first workflow.

```text
┌────────────────────────────────────────────┐
│              DATAPULSE DASHBOARD           │
├────────────────────────────────────────────┤
│                                            │
│  📊 KPIs          🚨 Alerts       🤖 AI    │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  📈 Trends          🔥 Correlations        │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  🚨 Anomalies       🔮 What-If             │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  💬 Natural Language Query                 │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  📄 Generate Professional Report           │
│                                            │
└────────────────────────────────────────────┘
```

---

# 🔄 Complete DataPulse Intelligence Pipeline

```text
                    ┌───────────────────┐
                    │   Raw Dataset     │
                    │   CSV/TXT/XLSX    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │    Data Loader    │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │   Data Cleaner    │
                    │                   │
                    │ • Missing Values  │
                    │ • Duplicates      │
                    │ • Data Types      │
                    │ • Dates           │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Analytics Engine  │
                    └─────────┬─────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       Statistics       Visualization     Correlation
             │                │                │
             └────────────────┼────────────────┘
                              │
             ┌────────────────┼────────────────┐
             │                │                │
             ▼                ▼                ▼
       What-If           Anomaly          NLP Query
       Simulator        Detection          Engine
             │                │                │
             └────────────────┼────────────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │  AI Insight       │
                    │     Engine        │
                    └─────────┬─────────┘
                              │
                 ┌────────────┴────────────┐
                 │                         │
                 ▼                         ▼
          Local Math Mode            Cloud AI Mode
                 │                         │
                 └────────────┬────────────┘
                              ▼
                    ┌───────────────────┐
                    │ Decision Insights  │
                    └─────────┬─────────┘
                              │
                              ▼
                    ┌───────────────────┐
                    │ Modular PDF Report │
                    └───────────────────┘
```

---

# 🧠 Analytics Architecture

DataPulse follows a modular architecture so individual components can be improved independently.

```text
                    DATA SOURCE
                        │
                        ▼
                ┌───────────────┐
                │ Data Loader   │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Data Cleaner  │
                └───────┬───────┘
                        │
                        ▼
                ┌───────────────┐
                │ Data Processor│
                └───────┬───────┘
                        │
             ┌──────────┼──────────┐
             │          │          │
             ▼          ▼          ▼
        Statistics   Charts    Correlation
             │          │          │
             └──────────┼──────────┘
                        │
             ┌──────────┼──────────┐
             │          │          │
             ▼          ▼          ▼
         Anomaly     What-If      NLP
        Detection   Simulator    Query
             │          │          │
             └──────────┼──────────┘
                        │
                        ▼
                 AI Insights Engine
                        │
                        ▼
                 Decision Intelligence
                        │
                        ▼
                   PDF Reporting
```

---

# 🗃️ Dataset Structure

The original sales-oriented dataset follows this structure:

| Column       | Description          |
| ------------ | -------------------- |
| `Date`       | Transaction date     |
| `Product`    | Product name         |
| `Category`   | Product category     |
| `Region`     | Sales region         |
| `Units_Sold` | Number of units sold |
| `Unit_Price` | Price per unit       |
| `Sales`      | Total sales value    |
| `Profit`     | Profit generated     |

---

# 📌 Example Dataset

```csv
Date,Product,Category,Region,Units_Sold,Unit_Price,Sales,Profit
2026-01-03,Laptop,Electronics,East,12,55000,660000,72000
2026-01-08,Mouse,Accessories,West,45,800,36000,7200
2026-01-15,Keyboard,Accessories,North,32,1500,48000,9600
```

---

# 🏗️ Project Architecture

```text
DataPulse-Analytics-using-Matplotlib/
│
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── dashboard/
│   ├── migrations/
│   ├── static/
│   ├── templates/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   ├── views.py
│   └── tests.py
│
├── data/
│   ├── raw/
│   │   └── sales.csv
│   │
│   └── processed/
│       └── cleaned_sales.csv
│
├── src/
│   ├── data_loader.py
│   ├── data_cleaner.py
│   ├── data_processor.py
│   ├── statistics.py
│   ├── visualizations.py
│   ├── anomaly_detection.py
│   ├── correlation.py
│   ├── what_if.py
│   ├── natural_language_query.py
│   ├── ai_insights.py
│   └── report_generator.py
│
├── visualizations/
│   ├── category_sales_bar.png
│   ├── daily_sales_trend.png
│   ├── top_products_pie.png
│   ├── correlation_heatmap.png
│   └── anomaly_chart.png
│
├── reports/
│   ├── analysis_report.md
│   └── analysis_report.pdf
│
├── frontend/
│   └── static/
│       └── images/
│           └── dashboard.png
│
├── main.py
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── LICENSE
└── README.md
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Anubhav2321/DataPulse-Analytics-using-Matplotlib.git
cd DataPulse-Analytics-using-Matplotlib
```

---

## 2️⃣ Create a Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# 📦 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 4️⃣ Configure Environment Variables

If Cloud AI Mode is enabled, configure the required API credentials in your `.env` file.

Example:

```env
GROQ_API_KEY=your_api_key_here
```

> Never commit `.env` or API keys to GitHub.

Add this to `.gitignore`:

```text
.env
venv/
__pycache__/
*.pyc
```

---

# ▶️ 5️⃣ Run the Analytics Pipeline

```bash
python main.py
```

---

# 🌐 6️⃣ Run the Django Dashboard

Apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

Start the development server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 📸 Project Showcase

<p align="center">
  <img src="frontend/static/images/dashboard.png" alt="DataPulse Analytics Dashboard" width="100%" />
</p>

<p align="center">
  <i>DataPulse Analytics — Intelligent Data Analysis Dashboard</i>
</p>

---

# 📊 Visualization Gallery

### 📊 Category Sales

```text
visualizations/category_sales_bar.png
```

### 📈 Daily Sales Trend

```text
visualizations/daily_sales_trend.png
```

### 🥧 Top Products

```text
visualizations/top_products_pie.png
```

### 🔥 Correlation Heatmap

```text
visualizations/correlation_heatmap.png
```

### 🚨 Anomaly Analysis

```text
visualizations/anomaly_chart.png
```

---

# 🛠️ Technology Stack

<p align="center">

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
<img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
<img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
<img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" />
<img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
<img src="https://img.shields.io/badge/Groq-AI-orange?style=for-the-badge" />
<img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />

</p>

---

# 🧩 Feature Matrix

| Feature                    | Status |
| -------------------------- | ------ |
| Dataset Upload             | ✅      |
| CSV Support                | ✅      |
| TXT Support                | ✅      |
| XLSX Support               | ✅      |
| Automated Data Cleaning    | ✅      |
| Statistical Analysis       | ✅      |
| Matplotlib Visualization   | ✅      |
| KPI Dashboard              | ✅      |
| What-If Scenario Simulator | ✅      |
| Smart Anomaly Detection    | ✅      |
| Correlation Heatmap        | ✅      |
| Natural Language Query     | ✅      |
| AI Insights Engine         | ✅      |
| Local Math Mode            | ✅      |
| Cloud AI Mode              | ✅      |
| Groq Integration           | ✅      |
| KPI Threshold Alerts       | ✅      |
| Modular PDF Export         | ✅      |
| Analytical Markdown Report | ✅      |
| Django Dashboard           | ✅      |

---

# 🔒 Privacy Architecture

DataPulse is designed with privacy as an important part of its architecture.

```text
                 ┌──────────────────────┐
                 │    Privacy Setting   │
                 └──────────┬───────────┘
                            │
                 ┌──────────┴───────────┐
                 │                      │
                 ▼                      ▼
        ┌─────────────────┐    ┌─────────────────┐
        │ Local Math Mode │    │  Cloud AI Mode  │
        └────────┬────────┘    └────────┬────────┘
                 │                      │
                 ▼                      ▼
          Local Processing          Groq AI
                 │                      │
                 └──────────┬───────────┘
                            ▼
                       AI Insights
```

Local Math Mode is intended for workflows where users want the core calculations to remain local.

---

# 🎯 Use Cases

DataPulse can be useful for:

### 📊 Business Analytics

* Sales analysis
* Revenue tracking
* Profit analysis
* Category performance
* Product performance

### 🎓 Education

* Student datasets
* Marks analysis
* Attendance analysis
* Performance trends
* Statistical projects

### 🔬 Data Science

* Exploratory Data Analysis
* Correlation analysis
* Outlier detection
* Feature exploration
* Data visualization

### 🏢 Organizations

* KPI monitoring
* Automated reports
* Decision support
* Data quality monitoring

---

# 🚀 Future Roadmap

DataPulse is designed to evolve into a more complete data intelligence platform.

### Planned / Potential Improvements

* [ ] Interactive Plotly charts
* [ ] Advanced forecasting
* [ ] Time-series prediction
* [ ] Automated feature engineering
* [ ] More AI models
* [ ] Dataset comparison
* [ ] Multi-dataset analysis
* [ ] Custom dashboard builder
* [ ] Scheduled reports
* [ ] Advanced anomaly models
* [ ] Machine-learning based predictions
* [ ] User authentication
* [ ] Role-based access
* [ ] Cloud deployment
* [ ] Database-backed analytics
* [ ] More natural-language commands

---

# 👨‍💻 About the Developer

<p align="center">

<img src="https://img.shields.io/badge/Developer-Anubhav%20Samanta-00C853?style=for-the-badge" />

</p>

<p align="center">

### **Anubhav Samanta**

🎓 **BCA Student | Techno India University, West Bengal**

💻 **Full-Stack Developer**

🐍 **Python Developer**

📊 **Data Analytics & Data Visualization Enthusiast**

🤖 **Artificial Intelligence & Machine Learning Enthusiast**

🚀 Passionate about building practical software projects,
modern web applications, data-driven systems, and intelligent solutions.

</p>

---

# 🔗 Connect With Me

<p align="center">

<a href="https://github.com/Anubhav2321" target="_blank">
  <img src="https://img.shields.io/badge/GitHub-Anubhav2321-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>

<a href="https://www.linkedin.com/in/anubhav-samanta-187549379" target="_blank">
  <img src="https://img.shields.io/badge/LinkedIn-Anubhav%20Samanta-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>

</p>

---

# ⭐ Support the Project

If you find **DataPulse Analytics** useful or interesting:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Report bugs
* 💡 Suggest new features
* 📢 Share the project
* 🤝 Contribute to the project

Every star, suggestion, and contribution is greatly appreciated. ❤️

---

# 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for more information.

---

# 🏆 Project Credits

<p align="center">

### 📊 DataPulse Analytics

**Designed & Developed by Anubhav Samanta**

Built with ❤️ using:

**Python • Pandas • NumPy • Matplotlib • Django • AI**

</p>

---

<p align="center">

### ⚡ DataPulse Analytics

<i>
Turning raw data into intelligent insights,  
visualizations, simulations, and decisions.
</i>

</p>

---

<p align="center">

### ⭐ If you like DataPulse Analytics, don't forget to star the repository!

</p>
