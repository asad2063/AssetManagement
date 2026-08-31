import sqlite3
import json
from datetime import datetime

DB_NAME = "assets.db"

def create_database():
    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            asset_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            value REAL NOT NULL,
            purchase_date TEXT NOT NULL,
            department TEXT,
            location TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS asset_counter (
            id INTEGER PRIMARY KEY,
            last_number INTEGER NOT NULL
        )
    """)



    connection.commit()
    connection.close()

def initialize_asset_counter_db(last_number):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO asset_counter (id, last_number)
        VALUES (1, ?)
        """,
        (last_number,)
    )

    connection.commit()
    connection.close()

def migrate_json_to_sqlite(json_file="assets.json"):
    with open(json_file, "r", encoding="utf-8") as file:
        assets = json.load(file)

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    inserted = 0
    skipped = 0

    for asset in assets:
        asset_id = asset.get("asset_id")
        name = asset.get("name")
        category = asset.get("category")
        department = asset.get("department")
        location = asset.get("location")
        status = asset.get("status")

        # Convert value to float
        value = float(asset.get("value") or 0)

        # Normalize purchase date
        purchase_date = asset.get("purchase_date")

        try:
            purchase_date = datetime.strptime(
                purchase_date,
                "%d-%m-%Y"
            ).strftime("%d-%m-%Y")
        except (ValueError, TypeError):
            purchase_date = None

        try:
            cursor.execute(
                """
                INSERT INTO assets (
                    asset_id,
                    name,
                    category,
                    value,
                    purchase_date,
                    department,
                    location,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    asset_id,
                    name,
                    category,
                    value,
                    purchase_date,
                    department,
                    location,
                    status
                )
            )

            inserted += 1

        except sqlite3.IntegrityError:
            skipped += 1

    connection.commit()

    cursor.execute(
        """
        SELECT COUNT(*), COALESCE(SUM(value), 0)
        FROM assets
        """
    )

    count, total_value = cursor.fetchone()

    connection.close()

    print("\n--- Migration Result ---")
    print(f"Inserted: {inserted}")
    print(f"Skipped: {skipped}")
    print(f"SQLite Assets: {count}")
    print(f"SQLite Total Value: {total_value:,.2f}")

def get_all_assets():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            asset_id,
            name,
            category,
            value,
            purchase_date,
            department,
            location,
            status
        FROM assets
        ORDER BY asset_id
    """)

    rows = cursor.fetchall()
    connection.close()

    assets = []

    for row in rows:
        asset = {
            "asset_id": row[0],
            "name": row[1],
            "category": row[2],
            "value": row[3],
            "purchase_date": row[4],
            "department": row[5],
            "location": row[6],
            "status": row[7]
        }
        assets.append(asset)
    return assets

def add_asset_db(asset):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO assets (
            asset_id,
            name,
            category,
            value,
            purchase_date,
            department,
            location,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            asset["asset_id"],
            asset["name"],
            asset["category"],
            float(asset["value"]),
            asset["purchase_date"],
            asset.get("department"),
            asset.get("location"),
            asset.get("status")
        )
    )

    connection.commit()
    connection.close()

def update_asset_db(asset):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE assets
        SET
            name = ?,
            category = ?,
            value = ?,
            purchase_date = ?,
            department = ?,
            location = ?,
            status = ?
        WHERE asset_id = ?
        """,
        (
            asset["name"],
            asset["category"],
            float(asset["value"]),
            asset["purchase_date"],
            asset.get("department"),
            asset.get("location"),
            asset.get("status"),
            asset["asset_id"]
        )
    )

    connection.commit()
    connection.close()

def delete_asset_db(asset_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM assets
        WHERE asset_id = ?
        """,
        (asset_id,)
    )

    connection.commit()
    connection.close()

def get_asset_count():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM assets
        """
    )

    result = cursor.fetchone()

    connection.close()

    return result[0]

def get_next_asset_id():

    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT last_number
        FROM asset_counter
        WHERE id = 1
        """
    )

    result = cursor.fetchone()

    if result is None:
        last_number = 0
    else:
        last_number = result[0]

    next_number = last_number + 1

    cursor.execute(
        """
        UPDATE asset_counter
        SET last_number = ?
        WHERE id = 1
        """,
        (next_number,)
    )

    connection.commit()
    connection.close()

    return f"AST-{next_number:04d}"

def get_total_asset_value():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT SUM(value)
        FROM assets
        """
    )

    result = cursor.fetchone()

    connection.close()

    return result[0] or 0

def get_department_summary():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            department,
            COUNT(*),
            SUM(value)
        FROM assets
        GROUP BY department
        ORDER BY department
        """
    )

    results = cursor.fetchall()

    connection.close()

    return results


