# 📊 Marketing Campaign Performance Dashboard  

## 🔹 Overview  
This project is an **interactive dashboard** that analyzes marketing campaigns to assess their effectiveness.  
The goal is to help businesses make **data-driven decisions** by evaluating KPIs, comparing channels, understanding audience demographics, and identifying seasonal performance trends.  

---

## 🔹 Objectives  
- Measure the success of marketing campaigns using key metrics (CTR, CPC, CPA, ROAS).  
- Compare performance across marketing channels to optimize budget allocation.  
- Analyze demographic data (age, gender, location) to identify high- and low-performing segments.  
- Detect seasonal or time-based trends in campaign performance.  
- Provide clear visualizations and recommendations for future marketing strategies.  

---

## 🔹 Dataset  
The dataset includes:  
- **Campaign Information**: ID, name, start/end dates.  
- **Performance Metrics**: impressions, clicks, conversions, spend, revenue.  
- **Channel Details**: marketing channel type (e.g., social media, email, search).  
- **Demographics**: age group, gender, location of targeted users.  

---

## 🔹 Key Features  
✅ **KPI Summary** – Displays total impressions, clicks, conversions, spend, revenue, average CTR, and overall ROAS.  
✅ **Campaign Comparison** – Bar/line charts showing CTR, conversion rate, and ROAS across campaigns.  
✅ **Channel Performance** – Pie/bar charts illustrating budget distribution and ROAS by channel.  
✅ **Demographic Insights** – Conversions and revenue breakdown by age, gender, and location.  
✅ **Time-based Trends** – Line charts monitoring performance over weeks/months to highlight seasonal peaks.  

---

## 🔹 Expected Insights  
📌 **Top-performing campaigns & channels**: Identify campaigns with highest ROAS and conversion rates.  
📌 **Budget optimization**: Highlight channels with high cost but low ROAS for budget reallocation.  
📌 **Demographic responsiveness**: Understand which audience segments engage best.  
📌 **Seasonal patterns**: Detect times of the year with peak conversions.  

---

## 🔹 Tech Stack  
- **Python (Pandas, NumPy)** → Data cleaning & analysis.  
- **Matplotlib & Seaborn** → Visualizations inside Jupyter Notebook.  
- **Streamlit** → Interactive dashboard for end users.  
- **Excel** → Original dataset storage.  

---

## 🔹 How to Run  

### ▶️ Run in Jupyter Notebook  
1. Open `marketing_dashboard_step_by_step.ipynb`.  
2. Run all cells to generate KPIs and visualizations.  

### ▶️ Run as Streamlit App  
1. Save the code in a file, e.g., `marketing_dashboard.py`.  
2. Open terminal and navigate to the folder:  
   ```bash
   cd path/to/project
