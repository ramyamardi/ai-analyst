import pandas as pd
import numpy as np
import io


def load_csv(uploaded_file) -> pd.DataFrame:
    """Load a CSV file from Streamlit uploader."""
    return pd.read_csv(uploaded_file)


def get_column_types(df: pd.DataFrame) -> dict:
    """Categorize columns by type."""
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()
    return {
        "numeric": numeric_cols,
        "categorical": categorical_cols,
        "datetime": datetime_cols
    }


def get_quick_stats(df: pd.DataFrame) -> dict:
    """Compute quick stats for the overview."""
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    completeness = round((1 - missing_cells / total_cells) * 100, 1) if total_cells > 0 else 100
    duplicates = df.duplicated().sum()
    col_types = get_column_types(df)

    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "completeness": completeness,
        "missing_cells": int(missing_cells),
        "duplicates": int(duplicates),
        "numeric_cols": len(col_types["numeric"]),
        "categorical_cols": len(col_types["categorical"]),
    }


def clean_dataframe(df: pd.DataFrame, actions: list) -> tuple:
    """Apply selected cleaning actions to the dataframe."""
    df = df.copy()
    log = []

    for action in actions:
        if action == "drop_duplicates":
            before = len(df)
            df = df.drop_duplicates()
            removed = before - len(df)
            log.append(f"✅ Removed {removed} duplicate rows")

        elif action == "drop_missing_rows":
            before = len(df)
            df = df.dropna()
            removed = before - len(df)
            log.append(f"✅ Removed {removed} rows with missing values")

        elif action == "fill_numeric_median":
            numeric_cols = df.select_dtypes(include='number').columns
            for col in numeric_cols:
                missing = df[col].isnull().sum()
                if missing > 0:
                    df[col] = df[col].fillna(df[col].median())
                    log.append(f"✅ Filled {missing} missing values in '{col}' with median ({df[col].median():.2f})")

        elif action == "fill_categorical_mode":
            cat_cols = df.select_dtypes(include=['object', 'category']).columns
            for col in cat_cols:
                missing = df[col].isnull().sum()
                if missing > 0:
                    mode_val = df[col].mode()[0] if not df[col].mode().empty else "Unknown"
                    df[col] = df[col].fillna(mode_val)
                    log.append(f"✅ Filled {missing} missing values in '{col}' with mode ('{mode_val}')")

        elif action == "strip_whitespace":
            cat_cols = df.select_dtypes(include='object').columns
            for col in cat_cols:
                df[col] = df[col].str.strip()
            log.append(f"✅ Stripped whitespace from {len(cat_cols)} text columns")

        elif action == "standardize_column_names":
            old_cols = list(df.columns)
            df.columns = [c.lower().strip().replace(" ", "_").replace("-", "_") for c in df.columns]
            log.append(f"✅ Standardized column names (e.g., '{old_cols[0]}' → '{df.columns[0]}')")

    return df, log


def dataframe_to_csv_bytes(df: pd.DataFrame) -> bytes:
    """Convert dataframe to CSV bytes for download."""
    return df.to_csv(index=False).encode("utf-8")
