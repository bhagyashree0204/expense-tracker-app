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