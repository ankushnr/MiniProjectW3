"""
ETL Pipeline + Tests
--------------------
Fetches user data from a REST API, transforms it with pandas, and saves it to CSV.

Install dependencies:
    python -m pip install requests pandas pytest

Run the pipeline:
    python etl_pipeline.py

Run unit tests:
    python -m pytest etl_pipeline.py -v
"""

from pathlib import Path

import pandas as pd
import requests


API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_FILE = Path("data") / "users.csv"


def extract_data():
    """Fetch JSON data from the REST API."""
    response = requests.get(API_URL, timeout=15)
    response.raise_for_status()
    data = response.json()

    if not isinstance(data, list):
        raise ValueError("The API response should be a list.")

    return data


def transform_data(data):
    """Convert API records to a clean DataFrame."""
    if not data:
        return pd.DataFrame(columns=["id", "name", "username", "email"])

    df = pd.DataFrame(data)

    required_columns = ["id", "name", "username", "email"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    df = df[required_columns].copy()
    df["name"] = df["name"].fillna("").astype(str).str.strip()
    df["username"] = df["username"].fillna("").astype(str).str.strip()
    df["email"] = df["email"].fillna("").astype(str).str.strip().str.lower()
    df = df.drop_duplicates(subset=["id"])
    df = df.dropna(subset=["id"])
    df = df.sort_values("id").reset_index(drop=True)

    return df


def load_data(df, output_file=OUTPUT_FILE):
    """Save the transformed DataFrame to a CSV file."""
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_file, index=False)
    return output_file


def run_pipeline():
    """Run the complete Extract, Transform, Load pipeline."""
    print("Starting ETL pipeline...")

    data = extract_data()
    print(f"Extracted {len(data)} records.")

    df = transform_data(data)
    print(f"Transformed {len(df)} records.")

    output_file = load_data(df)
    print(f"Saved CSV file to: {output_file.resolve()}")
    print("\nPreview:")
    print(df.head().to_string(index=False))
    print("\nETL pipeline completed successfully.")


# Pytest-compatible unit tests. Run with: python -m pytest etl_pipeline.py -v
def test_transform_data_cleans_emails_and_whitespace():
    sample = [{
        "id": 1,
        "name": "  Alex Smith ",
        "username": " alex ",
        "email": " ALEX@EXAMPLE.COM ",
    }]
    result = transform_data(sample)

    assert result.loc[0, "name"] == "Alex Smith"
    assert result.loc[0, "username"] == "alex"
    assert result.loc[0, "email"] == "alex@example.com"


def test_transform_data_removes_duplicate_ids():
    sample = [
        {"id": 1, "name": "Alex", "username": "alex", "email": "a@example.com"},
        {"id": 1, "name": "Alex", "username": "alex", "email": "a@example.com"},
    ]
    result = transform_data(sample)

    assert len(result) == 1


def test_transform_data_returns_expected_columns_for_empty_input():
    result = transform_data([])

    assert list(result.columns) == ["id", "name", "username", "email"]
    assert result.empty


if __name__ == "__main__":
    try:
        run_pipeline()
    except requests.RequestException as exc:
        print(f"API request failed: {exc}")
        print("Check your internet connection and try again.")
    except (ValueError, KeyError) as exc:
        print(f"Pipeline failed: {exc}")
