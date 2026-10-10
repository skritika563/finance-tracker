# Expense & Income Tracker
### Created on : Aug 2025
A personal finance dashboard built using Python, Streamlit, Pandas, and Plotly. The application allows users to record income and expenses, automatically classify transactions by category, review monthly summaries, and visualize spending patterns.

## Features

- **Transaction management:** Add, view, and delete transactions.
- **Automatic categorization:** Classify Salary and Bonus as income and other supported categories as expenses.
- **Data cleaning:** Validate dates, categories, and amounts using Pandas.
- **CSV persistence:** Save and reload transaction data locally.
- **Financial dashboard:** View total income, expenses, and balance.
- **Interactive visualizations:** Explore spending trends and expense categories with Plotly.
- **Monthly summaries:** Filter transactions and analyze finances by month.
- **CSV export:** Download transaction records for further analysis.

## Tech Stack

- Python
- Streamlit
- Pandas
- Plotly

## Project Structure

```text
Expense-Income-Tracker/
├── app.py
├── utils/
│   ├── __init__.py
│   ├── data_processing.py
│   ├── storage.py
│   └── charts.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone this repository and navigate to its directory.
2. Create and activate a Python virtual environment.
3. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

5. Open the local URL displayed in your terminal.

## Data Storage

Transactions are stored locally in `transactions.csv`. The file is created when the application saves transaction data. It is excluded from version control to help protect personal financial information.

## Categorization Rules

- Salary → Income
- Bonus → Income
- Subletting → Income
- Rent Income → Income
- All other supported categories → Expense

These rules are defined in `utils/data_processing.py` and can be customized.

## Future Improvements

- User-defined categories and categorization rules
- Budget setting and budget-versus-actual reports
- Recurring transaction support
- Database integration
- Automated tests and improved validation
