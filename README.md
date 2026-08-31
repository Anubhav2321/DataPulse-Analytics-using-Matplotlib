# 📊 DataPulse Analytics
### *Data Visualization & Insight Engine powered by Python, Pandas & Matplotlib*

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-Numerical%20Computing-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-Web%20Dashboard-092E20?style=for-the-badge&logo=django&logoColor=white" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active%20Development-00C853?style=for-the-badge" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" />
</p>

---

## 🚀 What is DataPulse Analytics?

**DataPulse Analytics** is a Python-based data analysis and visualization platform designed to transform raw datasets into meaningful statistics, professional visualizations, and actionable insights.

The project combines a **modular Python analytics pipeline** with a **Django-powered web dashboard**, allowing datasets to be processed, analyzed, visualized, and converted into analytical reports.

Instead of treating data visualization as simply creating charts, DataPulse follows a complete:

> **Data → Cleaning → Processing → Analysis → Visualization → Insights**

workflow.

---

## 🖥️ Project Showcase

<p align="center">
  <img src="frontend/static/images/dashboard.png" alt="DataPulse Analytics Dashboard" width="100%" />
</p>

<p align="center">
  <i>DataPulse Analytics — Data Analysis & Visualization Dashboard</i>
</p>

---

## ✨ Core Features

### 📂 Dataset Upload & Processing

Upload datasets directly through the web dashboard and process them without manually modifying the Python source code.

### Supported formats

- 📄 CSV
- 📝 TXT
- 📊 XLSX

---

### 🧹 Automated Data Cleaning

The cleaning pipeline prepares raw data for analysis by handling common data-quality problems.

Features include:

- Duplicate detection and removal
- Missing-value handling
- Date conversion
- Data normalization
- Clean dataset generation
- Processed dataset export

---

### 📊 Statistical Analysis

DataPulse automatically calculates important statistics from the dataset.

Current analytics include:

- 💰 Total Revenue
- 📦 Total Units Sold
- 📈 Average Sale Value
- ⬆️ Highest Single Sale
- ⬇️ Lowest Single Sale
- 🏆 Top Performing Category
- 🥇 Best Selling Product

---

### 📈 Matplotlib Visualization Engine

The visualization engine converts processed data into clear graphical insights.

Current visualizations include:

#### 📊 Category Sales Bar Chart

Compares total sales across different product categories.

#### 📈 Daily Sales Trend

Visualizes sales movement over time and helps identify growth, decline, and fluctuations.

#### 🥧 Top Products Distribution

Shows the contribution of top-performing products to overall sales.

---

### 🌐 Django Analytics Dashboard

DataPulse includes a browser-based dashboard powered by Django.

The dashboard provides:

- Dataset upload
- Dataset preview
- Row and column statistics
- Dynamic chart generation
- Category-wise analytics
- Product-wise analytics
- Sales trend visualization
- Analytical result presentation

---

### 📋 Automated Insight Report

After processing the dataset, DataPulse generates an analytical Markdown report.

The report can contain:

- Key business insights
- Top category
- Best-selling product
- Total revenue
- Total units sold
- Average sale value
- Highest sale
- Lowest sale

This transforms the project from a simple visualization script into a complete **data analysis and reporting pipeline**.

---

# 🔄 Data Processing Pipeline

```text
                  ┌─────────────────┐
                  │   Raw Dataset   │
                  │  CSV/TXT/XLSX   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │   Data Loader   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  Data Cleaner   │
                  │                 │
                  │ • Duplicates    │
                  │ • Missing Data  │
                  │ • Date Parsing  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Data Processor  │
                  │                 │
                  │ • Categories    │
                  │ • Products      │
                  │ • Sales         │
                  └────────┬────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
      ┌─────────────────┐       ┌─────────────────┐
      │   Statistics    │       │  Visualization  │
      │                 │       │                 │
      │ • Revenue       │       │ • Bar Chart     │
      │ • Average       │       │ • Line Chart    │
      │ • Min / Max     │       │ • Pie Chart     │
      └────────┬────────┘       └────────┬────────┘
               │                         │
               └────────────┬────────────┘
                            ▼
                   ┌─────────────────┐
                   │  Insight Engine │
                   └────────┬────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Analytical      │
                   │ Report          │
                   └─────────────────┘
```
## 🧠 How the Analytics Engine Works
DataPulse separates the complete workflow into dedicated modules.

```text
Raw Data
   │
   ▼
Load
   │
   ▼
Clean
   │
   ▼
Process
   │
   ▼
Analyze
   │
   ▼
Visualize
   │
   ▼
Generate Insights
   │
   ▼
Final Report
```
This modular architecture makes the project easier to maintain, test, and extend.
---
## 🗃️ Dataset Structure

The included sales dataset follows the structure below:

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

## Example Dataset
```text
Date,Product,Category,Region,Units_Sold,Unit_Price,Sales,Profit
2026-01-03,Laptop,Electronics,East,12,55000,660000,72000
2026-01-08,Mouse,Accessories,West,45,800,36000,7200
2026-01-15,Keyboard,Accessories,North,32,1500,48000,9600
```
## 🏗️ Project Architecture
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
│   └── insights.py
│
├── visualizations/
│   ├── category_sales_bar.png
│   ├── daily_sales_trend.png
│   └── top_products_pie.png
│
├── reports/
│   └── analysis_report.md
│
├── frontend/
│   └── static/
│       └── images/
│           └── dashboard.png
│
├── main.py
├── manage.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── README.md
```
## 📦 Installation & Setup
1️⃣ Clone the Repository
```text
git clone https://github.com/Anubhav2321/DataPulse-Analytics-using-Matplotlib.git
cd DataPulse-Analytics-using-Matplotlib
```
---
2️⃣ Create a Virtual Environment
Windows
```text

python -m venv venv
```
Activate:
```text

venv\Scripts\activate
```
macOS / Linux
```
python3 -m venv venv
```
Activate:
```text

source venv/bin/activate
```
3️⃣ Install Dependencies
```
pip install -r requirements.txt
```
▶️ Running the Analytics Pipeline

Run:
```text

python main.py
```
---
## 🌐 Running the Django Dashboard
Apply Migrations
```text

python manage.py makemigrations
python manage.py migrate
```
Start the Development Server
```text

python manage.py runserver
```

Open your browser:
```text

http://127.0.0.1:8000/
```
## 📸 Visualization Gallery


Once the analytics pipeline has been executed, generated charts can be displayed directly inside this README.

📊 Category Sales


📈 Daily Sales Trend


🥧 Top Products
---
## 👨‍💻 About the Developer
Anubhav Samanta

- 🎓 BCA Student at Techno India University, West Bengal
- 💻 Full-Stack Developer

- 🐍 Python Developer

- 📊 Data Analytics & Data Visualization Enthusiast

- 🤖 Interested in Artificial Intelligence & Machine Learning

- 🚀 Passionate about building practical software projects, intelligent applications, and modern web-based systems.
---
---

# 👨‍💻 About the Developer

<p align="center">

  <img src="https://img.shields.io/badge/Developer-Anubhav%20Samanta-00C853?style=for-the-badge" />

</p>

<p align="center">

### Anubhav Samanta

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
    <img src="https://img.shields.io/badge/GitHub-Anubhav2321-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub" />
  </a>

  <a href="https://www.linkedin.com/in/anubhav-samanta-187549379" target="_blank">
    <img src="https://img.shields.io/badge/LinkedIn-Anubhav%20Samanta-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
  </a>

</p>

---

# 🛠️ Built With

<p align="center">

  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge&logo=matplotlib&logoColor=white" />
  <img src="https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white" />
  <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
  <img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white" />

</p>

---

# ⭐ Support the Project

If you find **DataPulse Analytics** useful, interesting, or helpful for learning, consider supporting the project:

- ⭐ **Star** the repository
- 🍴 **Fork** the project
- 🐛 **Report** bugs or issues
- 💡 **Suggest** new features
- 📢 **Share** the project with others

Every star, suggestion, and contribution is greatly appreciated! ❤️

---

# 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for more information.

---

# 🚀 Project Credits

<p align="center">

### 📊 DataPulse Analytics

**Designed & Developed by Anubhav Samanta**

Built with ❤️ using **Python, Pandas, NumPy, Matplotlib & Django**

</p>

<p align="center">

<em>
Turning raw data into meaningful insights through code, visualization, and analytics.
</em>

</p>

---

<p align="center">

### ⭐ If you like DataPulse Analytics, don't forget to star the repository!

</p>
