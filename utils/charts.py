import pandas as pd
import plotly.express as px


def income_expense_line_chart(df):
    """Daily income-versus-expense line chart."""
    if df.empty:
        return None

    daily = (
        df.groupby(["Date", "Type"], as_index=False)["Amount"]
        .sum()
        .sort_values("Date")
    )

    fig = px.line(
        daily,
        x="Date",
        y="Amount",
        color="Type",
        markers=True,
        title="Income vs Expenses Over Time",
        labels={"Amount": "Amount (₹)", "Date": "Date"},
        color_discrete_map={
            "Income": "#066C2B",
            "Expense": "#C80909",
        },
    )

    fig.update_layout(legend_title_text="Transaction Type")
    return fig


def expense_pie_chart(df):
    """Pie chart showing expenses by category."""
    expenses = df[df["Type"] == "Expense"]

    if expenses.empty:
        return None

    category_totals = (
        expenses.groupby("Category", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

    return px.pie(
        category_totals,
        names="Category",
        values="Amount",
        title="Expenses by Category",
        hole=0.35,
    )


def monthly_bar_chart(df):
    """Bar chart comparing income and expenses."""
    if df.empty:
        return None

    totals = (
        df.groupby("Type", as_index=False)["Amount"]
        .sum()
    )

    return px.bar(
        totals,
        x="Type",
        y="Amount",
        color="Type",
        title="Income vs Expenses for Selected Month",
        labels={"Amount": "Amount (₹)", "Type": "Transaction Type"},
        color_discrete_map={
            "Income": "#1EDBAC",
            "Expense": "#DB1E57",
        },
    )


def category_bar_chart(df):
    """Bar chart of expenses by category."""
    expenses = df[df["Type"] == "Expense"]

    if expenses.empty:
        return None

    category_totals = (
        expenses.groupby("Category", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=False)
    )

    return px.bar(
        category_totals,
        x="Category",
        y="Amount",
        title="Spending by Category",
        labels={"Amount": "Amount (₹)", "Category": "Category"},
    )
