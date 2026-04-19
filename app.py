import os
import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Expense Analytics Dashboard", layout="wide")

# ---------- SAFE DATA LOADING ----------
if not os.path.exists("data/cleaned_expenses.csv"):
    st.error("cleaned_expenses.csv not found. Please run: python main.py")
    st.stop()

df = pd.read_csv("data/cleaned_expenses.csv")

if df.empty:
    st.error("The cleaned expense dataset is empty.")
    st.stop()

if os.path.exists("data/monthly_forecast.csv"):
    forecast_df = pd.read_csv("data/monthly_forecast.csv")
else:
    forecast_df = pd.DataFrame({
        "Forecast_Month": ["Not available"],
        "Predicted_Spending": ["Run main.py first"]
    })

required_columns = ["amount", "category", "payment_method", "month"]
missing_cols = [col for col in required_columns if col not in df.columns]

if missing_cols:
    st.error(f"Missing columns in dataset: {missing_cols}")
    st.stop()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.title("Filters")

category_filter = st.sidebar.multiselect(
    "Select Category",
    options=sorted(df["category"].dropna().unique()),
    default=sorted(df["category"].dropna().unique())
)

payment_filter = st.sidebar.multiselect(
    "Select Payment Method",
    options=sorted(df["payment_method"].dropna().unique()),
    default=sorted(df["payment_method"].dropna().unique())
)

filtered_df = df[
    (df["category"].isin(category_filter)) &
    (df["payment_method"].isin(payment_filter))
].copy()

if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

# ---------- TITLE ----------
st.title("💸 Expense Analytics Dashboard")
st.caption("Interactive expense tracking, category analysis, and next-month forecast")

# ---------- KPI CARDS ----------
total_spend = filtered_df["amount"].sum()
avg_spend = filtered_df["amount"].mean()
top_category = filtered_df.groupby("category")["amount"].sum().idxmax()
transaction_count = len(filtered_df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("💰 Total Spending", f"{total_spend:,.0f}")
k2.metric("📊 Avg Transaction", f"{avg_spend:,.0f}")
k3.metric("🏆 Top Category", top_category)
k4.metric("🧾 Transactions", f"{transaction_count:,}")

st.markdown("---")

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["📊 Overview", "📈 Analysis", "🔮 Forecast"])

# ----------- TAB 1: OVERVIEW -----------
with tab1:
    st.subheader("Spending Distribution")

    c1, c2 = st.columns(2)

    category_df = filtered_df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
    payment_df = filtered_df.groupby("payment_method", as_index=False)["amount"].sum().sort_values("amount", ascending=False)

    fig1 = px.pie(
        category_df,
        names="category",
        values="amount",
        hole=0.45,
        title="Category Share"
    )
    c1.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        payment_df,
        x="payment_method",
        y="amount",
        text_auto=True,
        title="Payment Method Spend"
    )
    c2.plotly_chart(fig2, use_container_width=True)

    st.subheader("Top Categories Table")
    st.dataframe(category_df, use_container_width=True)

# ----------- TAB 2: ANALYSIS -----------
with tab2:
    st.subheader("Monthly Trend Analysis")

    monthly_df = filtered_df.groupby("month", as_index=False)["amount"].sum().sort_values("month")

    fig3 = px.line(
        monthly_df,
        x="month",
        y="amount",
        markers=True,
        title="Monthly Spending Trend"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Category Comparison")

    fig4 = px.bar(
        category_df,
        x="category",
        y="amount",
        text_auto=True,
        color="category",
        title="Category-wise Spending"
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Payment Method Breakdown")
    fig5 = px.bar(
        filtered_df,
        x="payment_method",
        y="amount",
        color="category",
        title="Payment Method vs Category"
    )
    st.plotly_chart(fig5, use_container_width=True)

# ----------- TAB 3: FORECAST -----------
with tab3:
    st.subheader("Future Spending Prediction")
    st.dataframe(forecast_df, use_container_width=True)

    st.subheader("Insights")

    highest_month = filtered_df.groupby("month")["amount"].sum().idxmax()
    highest_month_value = filtered_df.groupby("month")["amount"].sum().max()

    st.success(f"Total Spending: {total_spend:,.2f}")
    st.info(f"Average Transaction: {avg_spend:,.2f}")
    st.warning(f"Highest Spending Month: {highest_month} ({highest_month_value:,.2f})")

# ----------- RAW DATA -----------
st.markdown("---")
st.subheader("Raw Data Preview")
st.dataframe(filtered_df.head(50), use_container_width=True)