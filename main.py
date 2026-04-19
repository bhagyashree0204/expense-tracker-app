from src.utils import ensure_project_folders
from src.data_generator import generate_synthetic_expense_data
from src.database_manager import create_database, insert_expenses_from_csv, fetch_all_expenses, run_sql_query
from src.analysis import clean_data, category_analysis, monthly_analysis, payment_analysis, create_visualizations, generate_insights
from src.model import forecast_next_month

def main():
    ensure_project_folders()

    print("Step 1: Generating synthetic expense data...")
    generate_synthetic_expense_data(num_records=1500, output_path="data/expenses.csv")

    print("Step 2: Creating SQLite database...")
    create_database()

    print("Step 3: Loading CSV data into SQLite...")
    insert_expenses_from_csv("data/expenses.csv")

    print("Step 4: Reading expense data from database...")
    df = fetch_all_expenses()

    print("Step 5: Cleaning data...")
    df = clean_data(df)
    df.to_csv("data/cleaned_expenses.csv", index=False)

    print("Step 6: Running SQL query for validation...")
    sql_result = run_sql_query("""
        SELECT category, ROUND(SUM(amount), 2) AS total_spend
        FROM expenses
        GROUP BY category
        ORDER BY total_spend DESC
    """)
    print(sql_result)

    print("Step 7: Creating charts...")
    create_visualizations(df)

    print("Step 8: Generating insights...")
    insights = generate_insights(df)
    for insight in insights:
        print(insight)

    print("Step 9: Training ML model and forecasting next month spend...")
    forecast_df, mae, rmse, r2 = forecast_next_month(df)
    print(forecast_df)
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2 Score: {r2:.4f}")

    print("Step 10: Exporting Power BI data...")
    df.to_csv("data/powerbi_expenses.csv", index=False)

    print("Project completed successfully!")

if __name__ == "__main__":
    main()