import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


def clean_data(df):
    df = df.copy()

    df["expense_date"] = pd.to_datetime(df["expense_date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df.dropna(subset=["expense_date", "category", "amount", "payment_method"], inplace=True)
    df = df[df["amount"] > 0]

    df["month"] = df["expense_date"].dt.to_period("M").astype(str)
    df["month_num"] = df["expense_date"].dt.month
    df["year"] = df["expense_date"].dt.year
    df["weekday"] = df["expense_date"].dt.day_name()

    return df


def category_analysis(df):
    return df.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)


def monthly_analysis(df):
    return df.groupby("month", as_index=False)["amount"].sum().sort_values("month")


def payment_analysis(df):
    return df.groupby("payment_method", as_index=False)["amount"].sum().sort_values("amount", ascending=False)


def generate_insights(df):
    insights = []

    total_spend = df["amount"].sum()
    avg_spend = df["amount"].mean()
    top_category = df.groupby("category")["amount"].sum().idxmax()
    top_month = df.groupby("month")["amount"].sum().idxmax()

    insights.append(f"Total spending: {total_spend:.2f}")
    insights.append(f"Average transaction amount: {avg_spend:.2f}")
    insights.append(f"Highest spending category: {top_category}")
    insights.append(f"Highest spending month: {top_month}")

    monthly_spend = df.groupby("month")["amount"].sum()
    threshold = monthly_spend.mean() * 1.20
    overspending_months = monthly_spend[monthly_spend > threshold]

    if len(overspending_months) > 0:
        insights.append("Overspending detected in:")
        for month, amount in overspending_months.items():
            insights.append(f" - {month}: {amount:.2f}")
    else:
        insights.append("No overspending month detected.")

    return insights


def create_visualizations(df):
    os.makedirs("outputs", exist_ok=True)
    sns.set_style("whitegrid")

    category_df = category_analysis(df)
    monthly_df = monthly_analysis(df)
    payment_df = payment_analysis(df)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=category_df, x="category", y="amount")
    plt.title("Category-wise Spending")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig("outputs/category_spending.png")
    plt.close()

    plt.figure(figsize=(10, 6))
    sns.lineplot(data=monthly_df, x="month", y="amount", marker="o")
    plt.title("Monthly Spending Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("outputs/monthly_trend.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(data=payment_df, x="payment_method", y="amount")
    plt.title("Payment Method Analysis")
    plt.tight_layout()
    plt.savefig("outputs/payment_method.png")
    plt.close()