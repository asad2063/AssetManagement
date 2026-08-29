import re 
import json
import os
from datetime import datetime

DATA_FILE = "assets.json"
COUNTER_FILE = "asset_counter.json"

def load_assets():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                return json.load(file)
        except json.JSONDecodeError:
            return []
    else:
        return []

def save_assets(assets):
    with open(DATA_FILE, "w") as file:
        json.dump(assets, file, indent=4)

def show_menu():
    print("\n--- Asset Management System ---")
    print("1. Add Asset")
    print("2. List Assets")
    print("3. Edit Asset")
    print("4. Delete Asset")
    print("5. Exit")

def edit_asset(assets):
    if not assets:
        print("No assets available to edit.")
        return

    list_assets(assets)

    asset_id = input(
        "\nEnter Asset ID to edit, or C to cancel: "
    ).strip().upper()

    if asset_id == "C":
        print("Edit cancelled.")
        return

    selected_asset = None

    for asset in assets:
        if asset.get("asset_id") == asset_id:
            selected_asset = asset
            break

    if selected_asset is None:
        print("Asset ID not found.")
        return

# Edit the Name
    print("\nPress Enter to keep the existing value.")
    print("Type C to cancel the edit.")
    new_name = input(
        f"Name [{selected_asset['name']}]: "
    ).strip()
    if new_name.upper() == "C":
        print("Edit cancelled.")
        return
 # Edit the Category
    new_category = input(
        f"Category [{selected_asset['category']}]: "
    ).strip()
    if new_category.upper() == "C":
            print("Edit cancelled.")
            return

# Edit the Department
    new_department = input(
        f"Department [{selected_asset.get('department', 'Not recorded')}]: "
    ).strip()

    if new_department.lower() == "c":
        print("Edit cancelled.")
        return

    # Edit the Location
    new_location = input(
        f"Location [{selected_asset.get('location', 'Not recorded')}]: "
    ).strip()

    if new_location.lower() == "c":
        print("Edit cancelled.")
        return

    # Edit the status
    while True:
        current_status = selected_asset.get("status", " Not recorded")

        new_status = input(
            f"Status [{current_status}] (Active/Disposed): "
        ).strip()

        if new_status.lower() == "c":
            print("Edit cancelled.")
            return

        if not new_status:
            break

        if new_status.lower() == "active":
            new_status = "Active"
            break

        if new_status.lower() == "disposed":
            new_status = "Disposed"
            break

        print("Please enter Active or Disposed.")

# Edit the Value
    while True:
        new_value_text = input(
            f"Value [{float(selected_asset['value']):,.2f}]: "
        ).strip()

        # C = cancel the whole edit
        if new_value_text.lower() == "c":
            print("Edit cancelled.")
            return

        # Blank = keep the existing value
        if not new_value_text:
            new_value = None
            break

        # Remove commas before validation
        clean_value = new_value_text.replace(",", "")

        # Allow digits with optional decimal point
        if not re.fullmatch(r"\d+(\.\d{1,2})?", clean_value):
            print(
                "Please enter a valid amount, "
                "for example 4000000 or 4,000,000.00."
            )
            continue

        new_value = float(clean_value)

        if new_value <= 0:
            print("Asset value must be greater than zero.")
            continue

        break

# Review proposed changes
    print("\n--- Review Proposed Changes ---")
    print(f"Asset ID: {selected_asset['asset_id']}")
    print(f"Name: {new_name or selected_asset['name']}")
    print(f"Category: " f"{new_category or selected_asset['category']}")
    print(f"Department: "f"{new_department or selected_asset.get('department', 'Not recorded')}")
    print(f"Location: "f"{new_location or selected_asset.get('location', 'Not recorded')}")
    print(f"Status: "f"{new_status or selected_asset.get('status', 'Not recorded')}")
    print(f"Value: {new_value or selected_asset['value']}")

    confirm = input("\nSave changes? (Y/N): ").strip().lower()

    if confirm != "y":
        print("Edit cancelled.")
        return

    if new_name:
        selected_asset["name"] = new_name

    if new_category:
        selected_asset["category"] = new_category

    if new_department:
        selected_asset["department"] = new_department

    if new_location:
        selected_asset["location"] = new_location

        

    if new_value:
        selected_asset["value"] = new_value

    save_assets(assets)

    print("Asset updated successfully.")

def get_valid_date(prompt):
    while True:
        date_text = input(prompt).strip()

        if date_text.lower() == "c":
            return None

        try:
            valid_date = datetime.strptime(date_text, "%d-%m-%Y")
            return valid_date.strftime("%d-%m-%Y")

        except ValueError:
            print("Please enter a valid date in DD-MM-YYYY format.")

def add_asset(assets):
    print("\n--- Add New Asset ---")
    print("Type C at any time to cancel.")

    # Asset name
    asset_name = input("Enter asset name: ").strip()

    if asset_name.lower() == "c":
        print("Asset entry cancelled.")
        return

    if not asset_name:
        print("Asset name cannot be blank.")
        return


    # Category
    category = input("Enter category: ").strip()

    if category.lower() == "c":
        print("Asset entry cancelled.")
        return

    if not category:
        print("Category cannot be blank.")
        return

    # Department
    department = input("Enter department: ").strip()

    if department.lower() == "c":
        print("Asset entry cancelled.")
        return

    if not department:
        print("Department cannot be blank.")
        return

    # Location
    location = input("Enter location: ").strip()

    if location.lower() == "c":
        print("Asset entry cancelled.")
        return

    if not location:
        print("Location cannot be blank.")
        return

    while True:
        status = input("Enter status (Active/Disposed): ").strip()

        if status.lower() == "c":
            print("Asset entry cancelled.")
            return

        if status.lower() == "active":
            status = "Active"
            break

        if status.lower() == "disposed":
            status = "Disposed"
            break

        print("Please enter Active or Disposed.")

    # Purchase date
    purchase_date = get_valid_date("Enter purchase date (DD-MM-YYYY): ")

    if purchase_date is None:
        print("Asset entry cancelled.")
        return

    # Asset value with validation
    while True:
        value_text = input("Enter asset value: ").strip()

        if value_text.lower() == "c":
            print("Asset entry cancelled.")
            return

        if not value_text:
            print("Asset value cannot be blank.")
            continue

        # Remove commas before validation
        clean_value = value_text.replace(",", "")

        # Allow digits with optional decimal point
        if not re.fullmatch(r"\d+(\.\d{1,2})?", clean_value):
            print(
                "Please enter a valid amount, "
                "for example 4000000 or 4,000,000.00"
            )
            continue

        value = float(clean_value)

        if value <= 0:
            print("Asset value must be greater than zero.")
            continue

        break

    # Review before saving
    print("\nPlease review the asset:")
    print(f"Name: {asset_name}")
    print(f"Category: {category}")
    print(f"Department: {department}")
    print(f"Location: {location}")
    print(f"Status: {status}")
    print(f"Purchase Date: {purchase_date}")
    print(f"Value: {value:,.2f}")

    confirm = input("\nSave this asset? (Y/N): ").strip().lower()

    if confirm != "y":
        print("Asset entry cancelled.")
        return

    # Create asset
    asset = {
        "asset_id": generate_asset_id(),
        "name": asset_name,
        "category": category,
        "department": department,
        "location": location,
        "status": status,
        "purchase_date": purchase_date,
        "value": value
    }

    assets.append(asset)
    save_assets(assets)

    print(f"Asset {asset['asset_id']} added successfully.")

def generate_asset_id():
    last_number = 0

    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r") as file:
                counter_data = json.load(file)
                last_number = counter_data.get("last_number", 0)

        except (json.JSONDecodeError, OSError):
            last_number = 0

    next_number = last_number + 1

    with open(COUNTER_FILE, "w") as file:
        json.dump(
            {"last_number": next_number},
            file,
            indent=4
        )

    return f"AST-{next_number:04d}"

def list_assets(assets):
    if not assets:
        print("No assets found.")
        return

    print("\n--- Asset List ---")

    for index, asset in enumerate(assets, start=1):
        print(f"\nAsset {index}")
        print(f"Asset ID: {asset.get('asset_id', 'Old Record')}")
        print(f"Name: {asset['name']}")
        print(f"Category: {asset['category']}")
        print(f"Department: " f"{asset.get('department', 'Not recorded')}")
        print(f"Location: " f"{asset.get('location', 'Not recorded')}")
        print(f"Status: {asset.get('status', 'Not recorded')}") 
        print(f"Purchase Date: " f"{asset.get('purchase_date', 'Not recorded')}")
        print(f"Value: {asset['value']}")

def delete_asset(assets):
    if not assets:
        print("No assets available to delete.")
        return

    list_assets(assets)

    asset_id = input(
        "\nEnter Asset ID to delete, or C to cancel: "
    ).strip().upper()

    if asset_id == "C":
        print("Deletion cancelled.")
        return

    selected_asset = None

    for asset in assets:
        if asset.get("asset_id") == asset_id:
            selected_asset = asset
            break

    if selected_asset is None:
        print("Asset ID not found.")
        return

    print("\nYou are about to delete:")
    print(f"Asset ID: {selected_asset['asset_id']}")
    print(f"Name: {selected_asset['name']}")
    print(f"Category: {selected_asset['category']}")
    print(f"Value: {selected_asset['value']}")

    confirm = input(
        "\nAre you sure you want to delete this asset? (Y/N): "
    ).strip().lower()

    if confirm == "y":
        assets.remove(selected_asset)
        save_assets(assets)

        print(f"Asset {asset_id} deleted successfully.")
    else:
        print("Deletion cancelled.")

def migrate_asset_ids(assets):
    changed = False

    existing_numbers = []

    for asset in assets:
        asset_id = asset.get("asset_id")

        if asset_id:
            number = int(asset_id.split("-")[1])
            existing_numbers.append(number)

    next_number = max(existing_numbers, default=0) + 1

    for asset in assets:
        if not asset.get("asset_id"):
            asset["asset_id"] = f"AST-{next_number:04d}"
            next_number += 1
            changed = True

    if changed:
        save_assets(assets)

    return assets

def initialize_asset_counter(assets):
    if os.path.exists(COUNTER_FILE):
        return

    highest_number = 0

    for asset in assets:
        asset_id = asset.get("asset_id")

        if asset_id:
            try:
                number = int(asset_id.split("-")[1])

                if number > highest_number:
                    highest_number = number

            except (ValueError, IndexError):
                pass

    with open(COUNTER_FILE, "w") as file:
        json.dump(
            {"last_number": highest_number},
            file,
            indent=4
        )

def main():
    assets = load_assets()
    assets = migrate_asset_ids(assets)
    initialize_asset_counter(assets)
    while True:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            add_asset(assets)

        elif choice == "2":
            list_assets(assets)

        elif choice == "3":
            edit_asset(assets)

        elif choice == "4":
            delete_asset(assets)

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()