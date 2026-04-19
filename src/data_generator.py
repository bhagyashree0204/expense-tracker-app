import pandas as pd
import numpy as np

def generate_synthetic_expense_data(num_records=1000, output_path="data/expenses.csv"):
    np.random.seed(42)

    date_range = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
    categories = ["Food", "Travel", "Rent", "Shopping", "Bills"]

    data = pd.DataFrame({
        "Date": np.random.choice(date_range, num_records),
        "Category": np.random.choice(categories, num_records),
        "Amount": np.random.randint(100, 5000, num_records),
        "Payment Method": np.random.choice(["Cash", "Card", "UPI"], num_records)
    })

    data.to_csv(output_path, index=False)
    return data