import pandas as pd
from pathlib import Path

# Exchange rate provided in the project requirements
GBP_TO_INR = 105.50

# Input and output paths
INPUT_FILE = Path("books.csv")
OUTPUT_FILE = Path("cleaned_books.csv")


def clean_data():
    # Load scraped data
    df = pd.read_csv(INPUT_FILE)

    print("Original dataset shape:", df.shape)

    # Remove duplicate books
    df.drop_duplicates(
        subset=["title", "category"],
        inplace=True
    )

    # Clean book titles
    df["title"] = df["title"].astype(str).str.strip()

    # Convert price to numeric
    df["price_gbp"] = pd.to_numeric(
        df["price_gbp"],
        errors="coerce"
    )

    # Convert rating to integer
    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

    # Convert availability to Boolean
    df["availability"] = (
        df["availability"]
        .astype(str)
        .str.lower()
        .map({
            "true": True,
            "false": False
        })
    )

    # Remove rows with missing essential values
    df.dropna(
        subset=[
            "title",
            "category",
            "price_gbp",
            "rating",
            "availability"
        ],
        inplace=True
    )

    # Keep ratings between 1 and 5
    df = df[
        df["rating"].between(1, 5)
    ]

    # Keep non-negative prices
    df = df[
        df["price_gbp"] >= 0
    ]

    df["rating"] = df["rating"].astype(int)
    df["availability"] = df["availability"].astype(bool)

    # Convert GBP to INR
    df["price_inr"] = (
        df["price_gbp"] * GBP_TO_INR
    ).round(2)

    # Save cleaned dataset
    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Cleaned dataset shape:", df.shape)
    print("Saved cleaned data to:", OUTPUT_FILE)
    print(df.head())


if __name__ == "__main__":
    clean_data()
