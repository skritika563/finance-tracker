from pathlib import Path
import pandas as pd
from utils.data_processing import COLUMNS, clean_transaction_data

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "transactions.csv"

def load_transactions():
    """Load saved transactions and clean the data."""
    if not DATA_FILE.exists():
        return pd.DataFrame(columns=COLUMNS)

    try:
        df = pd.read_csv(DATA_FILE)
        return clean_transaction_data(df)
    except (OSError, pd.errors.ParserError, UnicodeDecodeError) as error:
        raise RuntimeError(
            f"Could not read {DATA_FILE.name}: {error}"
        ) from error


def save_transactions(df):
    """Clean and save transactions to CSV."""
    cleaned_df = clean_transaction_data(df)
    cleaned_df.to_csv(DATA_FILE, index=False)


def clear_transactions():
    """Remove all saved transactions."""
    save_transactions(pd.DataFrame(columns=COLUMNS))
