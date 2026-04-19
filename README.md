# 💸 Expense Tracker App using Data Science

## 📌 Overview
This project is an end-to-end Expense Tracker built using **Python, MySQL, Machine Learning, and Streamlit**.  
It allows users to analyze spending patterns, visualize trends, and predict future expenses using data science techniques.

---

## 🎯 Problem Statement
Managing personal or business expenses manually is inefficient and lacks insights.  
This project solves that by providing:
- structured data storage
- automated analysis
- visual insights
- future expense prediction

---

## 🚀 Features

- 📊 Interactive dashboard using Streamlit  
- 🗄️ MySQL database integration  
- 📈 Monthly and category-wise spending analysis  
- 🧠 Machine Learning-based expense forecasting  
- 🎯 Category and payment method insights  
- 🔍 Real-time filtering using sidebar  
- 📉 Trend visualization with charts  
- 📦 Synthetic data generation  

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Plotly  
- **Machine Learning:** Scikit-learn  
- **Database:** MySQL  
- **Dashboard:** Streamlit  

---

## 📊 Dashboard Preview

## 📸 Screenshots

![Dashboard](images/dashboard.png)  
![Trend Analysis](images/trend.png)  
![Forecast](images/forecast.png)  

---

## 🧠 Machine Learning

- **Model Used:** Linear Regression  
- **Approach:** Time-based forecasting using lag features  
- **Features Used:**
  - Previous month spending  
  - Transaction count  
  - Average transaction value  
  - Category-wise spending  

- **Evaluation Metrics:**
  - MAE (Mean Absolute Error)  
  - RMSE (Root Mean Squared Error)  
  - R² Score  

---

## 🔄 Project Workflow

```text
Data Generation → MySQL Storage → Data Cleaning → Analysis → Visualization → ML Model → Dashboard