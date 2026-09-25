import sqlite3
import pandas as pd
from pathlib import Path

DATA_FILE = Path("cleaned_books.csv")
DB_FILE = Path("books.db")


def create_database():
    # Load cleaned data
    df = pd.read_csv(DATA_FILE)

    # Connect to SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # Create Categories table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT UNIQUE NOT NULL
        )
    """)

    # Create Books table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category_id INTEGER,
            price_gbp REAL,
            price_inr REAL,
            rating INTEGER,
            availability BOOLEAN,
            book_url TEXT,
            FOREIGN KEY (category_id)
                REFERENCES Categories(category_id)
        )
    """)

    # Clear existing records so rerunning won't duplicate books
    cursor.execute("DELETE FROM Books")
    cursor.execute("DELETE FROM Categories")

    # Insert unique categories
    categories = df["category"].dropna().unique()

    for category in categories:
        cursor.execute(
            "INSERT INTO Categories (category_name) VALUES (?)",
            (category,)
        )

    # Create category name -> category ID mapping
    cursor.execute("""
        SELECT category_id, category_name
        FROM Categories
    """)

    category_map = {
        name: category_id
        for category_id, name in cursor.fetchall()
    }

    # Insert books
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Books (
                title,
                category_id,
                price_gbp,
                price_inr,
                rating,
                availability,
                book_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            row["title"],
            category_map[row["category"]],
            row["price_gbp"],
            row["price_inr"],
            int(row["rating"]),
            int(bool(row["availability"])),
            row["book_url"]
        ))

    conn.commit()

    # Verify database
    cursor.execute("SELECT COUNT(*) FROM Books")
    book_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Categories")
    category_count = cursor.fetchone()[0]

    print("Database created successfully!")
    print("Total books:", book_count)
    print("Total categories:", category_count)

    conn.close()


if __name__ == "__main__":
    create_database()
