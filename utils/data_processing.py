import pandas as pd

CATEGORIES = [
    "Salary",
    "Rental Income",
    "Subletting",
    "Rent & Maintainence",
    "Food",
    "Groceries & Utilities",
    "Shopping",
    "Travel",
    "Bonus",
    "Bills and Recharges",
    "Others",
]

INCOME_CATEGORIES = {"Salary", "Bonus", "Rental Income", "Subletting"}

COLUMNS = ["Date", "Type", "Category", "Amount", "Month"]


def get_transaction_type(category):
    return (
        "Income" if category in INCOME_CATEGORIES else "Expense"
    )


def clean_transaction_data(df):
    df = df.copy()

    for column in COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[COLUMNS]

    # Standardize dates and amounts.
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Category"] = df["Category"].astype("string").str.strip()
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # Remove incomplete or invalid transactions.
    df = df.dropna(subset=["Date", "Category", "Amount"])
    df = df[df["Category"].isin(CATEGORIES)]
    df = df[df["Amount"] > 0].copy()

    # Automatic Categorization of Type
    df["Type"] = df["Category"].apply(get_transaction_type)

    # Generate Month from Date to keep it consistent.
    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    return (
        df.sort_values("Date", ascending=False)
        .reset_index(drop=True)
    )


def create_transaction(transaction_date, category, amount):
    amount = float(amount)

    if category not in CATEGORIES:
        raise ValueError("Please select a valid category.")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    transaction_date = pd.to_datetime(transaction_date)
   
    return {
        "Date": transaction_date,
        "Type": get_transaction_type(category),
        "Category": category,
        "Amount": amount,
        "Month": transaction_date.strftime("%Y-%m"),
    }


def get_financial_summary(df):
    """Calculate total income, expenses, and balance."""
    income = df.loc[df["Type"] == "Income", "Amount"].sum()
    expenses = df.loc[df["Type"] == "Expense", "Amount"].sum()

    return {
        "income": float(income),
        "expenses": float(expenses),
        "balance": float(income - expenses),
    }


def get_monthly_summary(df):
    """Aggregate income and expenses for each month."""
    if df.empty:
        return pd.DataFrame(
            columns=["Month", "Income", "Expense", "Balance"]
        )

    summary = (
        df.pivot_table(
            index="Month",
            columns="Type",
            values="Amount",
            aggfunc="sum",
            fill_value=0,
        )
        .reset_index()
    )

    for column in ["Income", "Expense"]:
        if column not in summary.columns:
            summary[column] = 0.0

    summary["Balance"] = summary["Income"] - summary["Expense"]

    return summary[["Month", "Income", "Expense", "Balance"]].sort_values(
        "Month"
    )
