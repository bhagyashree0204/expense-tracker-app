import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def prepare_monthly_features(df):
    # Monthly total spend
    monthly_total = df.groupby("month", as_index=False)["amount"].sum()
    monthly_total = monthly_total.rename(columns={"amount": "total_spend"})

    # Monthly transaction count
    monthly_count = (
        df.groupby("month", as_index=False)["amount"]
        .count()
        .rename(columns={"amount": "transaction_count"})
    )

    # Monthly average transaction amount
    monthly_avg = (
        df.groupby("month", as_index=False)["amount"]
        .mean()
        .rename(columns={"amount": "avg_transaction_amount"})
    )

    # Monthly category totals
    category_monthly = pd.pivot_table(
        df,
        values="amount",
        index="month",
        columns="category",
        aggfunc="sum",
        fill_value=0
    ).reset_index()

    # Merge all monthly features
    features = monthly_total.merge(monthly_count, on="month")
    features = features.merge(monthly_avg, on="month")
    features = features.merge(category_monthly, on="month")

    # Sort by month
    features["month_date"] = pd.to_datetime(features["month"])
    features = features.sort_values("month_date").reset_index(drop=True)

    # Create lag features from previous month
    feature_cols = [col for col in features.columns if col not in ["month", "month_date", "total_spend"]]

    lag_df = pd.DataFrame()
    lag_df["month"] = features["month"]
    lag_df["month_date"] = features["month_date"]
    lag_df["target_total_spend"] = features["total_spend"]

    # Previous month total spend as feature
    lag_df["prev_total_spend"] = features["total_spend"].shift(1)

    # Previous month all other features
    for col in feature_cols:
        lag_df[f"prev_{col}"] = features[col].shift(1)

    # Month number as a time signal
    lag_df["month_num"] = lag_df["month_date"].dt.month
    lag_df["year"] = lag_df["month_date"].dt.year

    # Drop first row because it has no previous month
    lag_df = lag_df.dropna().reset_index(drop=True)

    return lag_df


def train_spending_prediction_model(df):
    features = prepare_monthly_features(df)

    if len(features) < 6:
        raise ValueError("Not enough monthly data to train the model. Generate more data first.")

    X = features.drop(columns=["month", "month_date", "target_total_spend"])
    y = features["target_total_spend"]

    # Train-test split preserving time order
    split_index = int(len(features) * 0.8)

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    results = pd.DataFrame({
        "Actual": y_test.values,
        "Predicted": np.round(predictions, 2)
    })

    return model, features, results, mae, rmse, r2


def forecast_next_month(df):
    model, features, results, mae, rmse, r2 = train_spending_prediction_model(df)

    latest_row = features.iloc[-1:].copy()

    # Build next-month input using latest known month as previous-month features
    X_next = latest_row.drop(columns=["month", "month_date", "target_total_spend"]).copy()

    # Move to next month for calendar features
    next_month_date = latest_row["month_date"].iloc[0] + pd.offsets.MonthBegin(1)
    X_next["month_num"] = next_month_date.month
    X_next["year"] = next_month_date.year

    predicted_spend = model.predict(X_next)[0]

    forecast_df = pd.DataFrame({
        "Forecast_Month": [next_month_date.strftime("%Y-%m")],
        "Predicted_Spending": [round(predicted_spend, 2)]
    })

    os.makedirs("outputs", exist_ok=True)
    os.makedirs("data", exist_ok=True)

    forecast_df.to_csv("data/monthly_forecast.csv", index=False)

    with open("outputs/model_results.txt", "w", encoding="utf-8") as f:
        f.write("Model Evaluation\n")
        f.write(f"MAE: {mae:.2f}\n")
        f.write(f"RMSE: {rmse:.2f}\n")
        f.write(f"R2 Score: {r2:.4f}\n\n")
        f.write("Predictions vs Actual\n")
        f.write(results.to_string(index=False))

    return forecast_df, mae, rmse, r2