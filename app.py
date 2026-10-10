import pandas as pd
import streamlit as st

from utils.data_processing import (
    CATEGORIES,
    create_transaction,
    get_financial_summary,
    get_monthly_summary,
    clean_transaction_data,
)
from utils.storage import (
    load_transactions,
    save_transactions,
    clear_transactions,
)
from utils.charts import (
    income_expense_line_chart,
    expense_pie_chart,
    monthly_bar_chart,
    category_bar_chart,
)


st.set_page_config(
    page_title="Expense & Income Tracker",
    page_icon="\u20B9",
    layout="wide",
)


# Session state 
if "transactions" not in st.session_state:
    st.session_state.transactions = load_transactions()

if "confirm_clear" not in st.session_state:
    st.session_state.confirm_clear = False


# Helper functions 
def refresh_transactions():
    """Clean, save, and refresh the in-memory transactions."""
    cleaned = clean_transaction_data(st.session_state.transactions)
    save_transactions(cleaned)
    st.session_state.transactions = cleaned

def show_metrics(df):
    """Display income, expenses, and balance."""
    summary = get_financial_summary(df)

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{summary['income']:,.2f}")
    col2.metric("Total Expenses", f"₹{summary['expenses']:,.2f}")
    col3.metric("Balance", f"₹{summary['balance']:,.2f}")


def show_transactions(df, key_prefix):
    """Display transactions and allow deletion of one selected row."""
    if df.empty:
        st.info("No transactions found.")
        return

    display_df = df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")

    st.dataframe(
        display_df[["Date", "Type", "Category", "Amount", "Month"]],
        use_container_width=True,
        hide_index=True,
    )

    # Use row positions to identify the exact transaction.
    row_positions = list(range(len(df)))

    def format_transaction(position):
        row = df.iloc[position]
        return (
            f"{row['Date']:%Y-%m-%d} | "
            f"{row['Type']} | {row['Category']} | "
            f"₹{row['Amount']:,.2f}"
        )

    selected_position = st.selectbox(
        "Select a transaction to delete",
        options=row_positions,
        format_func=format_transaction,
        key=f"{key_prefix}_delete_selection",
    )

    if st.button("Delete Selected Transaction", key=f"{key_prefix}_delete"):
        actual_index = df.index[selected_position]

        # Drop the exact underlying row, even if duplicate transactions exist.
        updated = st.session_state.transactions.drop(
            index=actual_index
        )
        st.session_state.transactions = updated.reset_index(drop=True)

        refresh_transactions()
        st.success("Transaction deleted.")
        st.rerun()


# Sidebar navigation 
st.sidebar.title("💰 Finance Tracker")
page = st.sidebar.radio(
    "Navigation",
    [
        "Add Transaction",
        "Dashboard",
        "Monthly Summary",
        "Export Data",
    ],
)
st.title("Expense & Income Tracker")
transactions = st.session_state.transactions


# Add Transaction 
if page == "Add Transaction":
    st.subheader("Add a Transaction")

    with st.form("transaction_form"):
        transaction_date = st.date_input("Date")
        category = st.selectbox("Category", CATEGORIES)
        amount = st.number_input(
            "Amount (₹)",
            min_value=0.01,
            value=100.00,
            step=10.00,
        )

        transaction_type = (
            "Income" if category in {"Salary", "Bonus"} else "Expense"
        )
        st.info(f"This category will be recorded as **{transaction_type}**.")

        submitted = st.form_submit_button("Add Transaction")

    if submitted:
        try:
            new_transaction = create_transaction(
                transaction_date,
                category,
                amount,
            )

            updated = pd.concat(
                [
                    st.session_state.transactions,
                    pd.DataFrame([new_transaction]),
                ],
                ignore_index=True,
            )

            st.session_state.transactions = updated
            refresh_transactions()

            st.success("Transaction added successfully!")
            st.rerun()

        except (ValueError, TypeError) as error:
            st.error(str(error))

    st.divider()
    st.subheader("All Transactions")
    show_transactions(
        st.session_state.transactions,
        "all_transactions",
    )


# Dashboard 
elif page == "Dashboard":
    st.subheader("Financial Overview")

    if transactions.empty:
        st.info("Add your first transaction to see your dashboard.")
    else:
        show_metrics(transactions)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            line_chart = income_expense_line_chart(transactions)
            if line_chart is not None:
                st.plotly_chart(line_chart, use_container_width=True)

        with col2:
            pie_chart = expense_pie_chart(transactions)
            if pie_chart is not None:
                st.plotly_chart(pie_chart, use_container_width=True)
            else:
                st.info("No expenses available for the category chart.")

        category_chart = category_bar_chart(transactions)
        if category_chart is not None:
            st.plotly_chart(category_chart, use_container_width=True)

        st.subheader("Monthly Financial Summary")
        st.dataframe(
            get_monthly_summary(transactions),
            use_container_width=True,
            hide_index=True,
        )


# Monthly Summary 

elif page == "Monthly Summary":
    st.subheader("Monthly Summary")

    if transactions.empty:
        st.info("No transactions available yet.")
    else:
        months = sorted(
            transactions["Month"].dropna().unique().tolist(),
            reverse=True,
        )

        selected_month = st.selectbox("Select Month", months)
        monthly_df = transactions[
            transactions["Month"] == selected_month
        ].copy()

        show_metrics(monthly_df)
        monthly_chart = monthly_bar_chart(monthly_df)

        if monthly_chart is not None:
            st.plotly_chart(monthly_chart, use_container_width=True)

        st.subheader(f"Transactions for {selected_month}")
        show_transactions(monthly_df, "monthly_transactions")


# Export Data 
elif page == "Export Data":
    st.subheader("Export Your Data")

    if transactions.empty:
        st.info("There are no transactions to export.")
    else:
        csv_data = transactions.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Transactions as CSV",
            data=csv_data,
            file_name="transactions.csv",
            mime="text/csv",
        )

    st.divider()
    st.subheader("Clear All Transactions")

    st.warning(
        "This permanently clears the locally saved transaction data. "
        "Download a backup first if you need one."
    )

    if not st.session_state.confirm_clear:
        if st.button("Clear All Data", type="secondary"):
            st.session_state.confirm_clear = True
            st.rerun()
    else:
        st.error("Are you sure? This action cannot be undone.")

        confirm_col, cancel_col = st.columns(2)

        with confirm_col:
            if st.button("Yes, Clear Everything"):
                clear_transactions()
                st.session_state.transactions = load_transactions()
                st.session_state.confirm_clear = False
                st.success("All transactions have been cleared.")
                st.rerun()

        with cancel_col:
            if st.button("Cancel"):
                st.session_state.confirm_clear = False
                st.rerun()
