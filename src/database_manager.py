import pandas as pd
import mysql.connector


def create_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS expense_tracker")
    cursor.execute("USE expense_tracker")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            expense_id INT PRIMARY KEY AUTO_INCREMENT,
            expense_date DATE,
            category VARCHAR(100),
            amount DECIMAL(10,2),
            payment_method VARCHAR(50),
            description VARCHAR(255)
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()


def insert_expenses_from_csv(csv_path="data/expenses.csv"):
    df = pd.read_csv(csv_path)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_tracker"
    )
    cursor = conn.cursor()

    insert_query = """
        INSERT INTO expenses (expense_date, category, amount, payment_method, description)
        VALUES (%s, %s, %s, %s, %s)
    """

    for _, row in df.iterrows():
        expense_date = pd.to_datetime(row["Date"]).date()
        category = row["Category"]
        amount = float(row["Amount"])
        payment_method = row["Payment Method"]
        description = row["Description"] if "Description" in df.columns else None

        cursor.execute(insert_query, (expense_date, category, amount, payment_method, description))

    conn.commit()
    cursor.close()
    conn.close()


def fetch_all_expenses():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_tracker"
    )

    query = "SELECT * FROM expenses"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def run_sql_query(query):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_tracker"
    )

    result = pd.read_sql(query, conn)
    conn.close()
    return result