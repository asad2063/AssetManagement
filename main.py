import re 
from datetime import datetime, date

from database import (
    get_next_asset_id,
    get_department_summary,
    initialize_asset_counter_db,
    create_database,
    get_all_assets,
    add_asset_db,
    update_asset_db,
    delete_asset_db,
    get_asset_count,
    get_total_asset_value
)

create_database()
initialize_asset_counter_db(14)

def show_menu():

    print("1. Add Asset")
    print("2. List Assets")
    print("3. Edit Asset")
    print("4. Delete Asset")
    print("5. Search Asset")
    print("6. Filter Assets")
    print("7. Reports")
    print("8. Exit")

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

# Edit the Purchase Date
    while True:
        current_purchase_date = (
            selected_asset.get("purchase_date")
            or "Not recorded"
        )

        new_purchase_date = input(
            f"Purchase Date [{current_purchase_date}] "
            "(DD-MM-YYYY): "
        ).strip()

        if new_purchase_date.lower() == "c":
            print("Edit cancelled.")
            return

        # Blank = keep existing date
        if not new_purchase_date:
            break

        if not re.fullmatch(r"\d{2}-\d{2}-\d{4}", new_purchase_date):
            print(
                "Please enter the date exactly in DD-MM-YYYY format, "
                "for example 23-04-2024."
            )
            continue

        try:
            purchase_date_obj = datetime.strptime(
                new_purchase_date,
                "%d-%m-%Y"
            ).date()

        except ValueError:
            print(
                "Please enter a valid date in DD-MM-YYYY format, "
                "for example 01-01-2026."
            )
            continue

        if purchase_date_obj > date.today():
            print("Purchase date cannot be in the future.")
            continue

        break

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
    print(f"Purchase Date: "f"{new_purchase_date or selected_asset.get('purchase_date') or 'Not recorded'}")
    print(f"Value: {new_value or selected_asset['value']:,.2f}")

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

    if new_status:
        selected_asset["status"] = new_status

    if new_purchase_date:
        selected_asset["purchase_date"] = new_purchase_date        

    if new_value:
        selected_asset["value"] = new_value

    update_asset_db(selected_asset)
#   

    print("Asset updated successfully.")

def get_valid_date(prompt):
    while True:
        date_text = input(prompt).strip()

        if date_text.lower() == "c":
            return None

        try:
            valid_date = datetime.strptime(
                date_text,
                "%d-%m-%Y"
            ).date()

            if valid_date > date.today():
                print("Purchase date cannot be in the future.")
                continue

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
    add_asset_db(asset)

    print(f"Asset {asset['asset_id']} added successfully.")

def generate_asset_id():
    return get_next_asset_id()

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
    print(f"Value: {selected_asset['value']:,.2f}")

    confirm = input(
        "\nAre you sure you want to delete this asset? (Y/N): "
    ).strip().lower()

    if confirm == "y":
        delete_asset_db(selected_asset["asset_id"])
#       assets.remove(selected_asset)
#       

        print(f"Asset {asset_id} deleted successfully.")
    else:
        print("Deletion cancelled.")

def search_asset(assets):
    while True:
        search_term = input(
            "\nEnter Asset ID or Asset Name to search "
            "(Enter for None, C to return): "
        ).strip()

        if search_term.lower() == "c":
            return

        found = False

        for asset in assets:
            asset_id = str(asset.get("asset_id") or "")
            asset_name = asset.get("asset_name") or asset.get("name")

            # Enter or "none" finds assets with no name
            if search_term == "" or search_term.lower() == "none":
                match = (
                    asset_name is None
                    or str(asset_name).strip() == ""
                )

            # Normal search by Asset ID or Name
            else:
                search_lower = search_term.lower()

                match = (
                    search_lower in asset_id.lower()
                    or search_lower in str(asset_name or "").lower()
                )

            if match:
                print("\nAsset Found:")
                print(f"Asset ID: {asset.get('asset_id')}")
                print(f"Name: {asset_name}")
                print(f"Category: {asset.get('category')}")
                print(f"Value: {asset.get('value'):,.2f}")
                print(f"Department: {asset.get('department')}")
                print(f"Location: {asset.get('location')}")
                print(f"Status: {asset.get('status')}")
                print("-" * 30)

                found = True

        if not found:
            print("No matching assets found.")

def filter_assets(assets):
    while True:
        print("\n--- Filter Assets ---")
        print("1. Department")
        print("2. Location")
        print("3. Category")
        print("4. Status")
        print("C. Return to Main Menu")

        filter_choice = input("Enter filter choice: ").strip().lower()

        if filter_choice == "c":
            return

        if filter_choice == "1":
            field = "department"
        elif filter_choice == "2":
            field = "location"
        elif filter_choice == "3":
            field = "category"
        elif filter_choice == "4":
            field = "status"
        else:
            print("Invalid filter choice.")
            continue





        filter_value = input(
            f"Enter {field} to filter "
            "(Enter for None, C to return): "
        ).strip()

        if filter_value.lower() == "c":
            continue

        found = False

        for asset in assets:
            asset_value = asset.get(field)

            # Empty input or "none" finds missing/blank values
            if filter_value == "" or filter_value.lower() == "none":
                match = asset_value is None or str(asset_value).strip() == ""
            else:
                match = filter_value.lower() in str(asset_value or "").lower()

            if match:
                print("\nAsset Found:")
                print(f"Asset ID: {asset.get('asset_id')}")
                print(f"Name: {asset.get('asset_name') or asset.get('name')}")
                print(f"Category: {asset.get('category')}")
                print(f"Value: {asset.get('value')}")
                print(f"Department: {asset.get('department')}")
                print(f"Location: {asset.get('location')}")
                print(f"Status: {asset.get('status')}")
                print("-" * 30)

                found = True

        if not found:
            print("No matching assets found.")





        if filter_value.lower() == "c":
            continue

        filter_value = filter_value.lower()
        found = False

        for asset in assets:
            asset_value = str(asset.get(field, "")).lower()

            if filter_value in asset_value:
                print("\nAsset Found:")
                print(f"Asset ID: {asset.get('asset_id')}")
                print(
                    f"Name: "
                    f"{asset.get('asset_name') or asset.get('name')}"
                )
                print(f"Category: {asset.get('category')}")
                print(f"Value: {asset.get('value')}")
                print(f"Department: {asset.get('department')}")
                print(f"Location: {asset.get('location')}")
                print(f"Status: {asset.get('status')}")
                print("-" * 30)

                found = True

        if not found:
            print("No matching assets found.")

def asset_summary(assets):
    total_assets = len(assets)

    total_value = 0
    active_count = 0
    active_value = 0
    disposed_count = 0
    disposed_value = 0
    no_status_count = 0
    no_status_value = 0

    for asset in assets:
        value = asset.get("value") or 0

        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0
        
        status = str(asset.get("status") or "").lower()

        total_value += value

        if status == "active":
            active_count += 1
            active_value += value

        elif status == "disposed":
            disposed_count += 1
            disposed_value += value

        else:
            no_status_count += 1
            no_status_value += value

    print("\n--- Asset Summary Report ---")
    print(f"Total Assets: {total_assets}")
    print(f"Total Value: {total_value:,.2f}")
    print("-" * 30)
    print(f"Active Assets: {active_count}")
    print(f"Active Value: {active_value:,.2f}")
    print("-" * 30)
    print(f"Disposed Assets: {disposed_count}")
    print(f"Disposed Value: {disposed_value:,.2f}")
    print("-" * 30)
    print(f"Status Not Recorded: {no_status_count}")
    print(f"Value Not Classified: {no_status_value:,.2f}")
    print("-" * 30)
    
# Control Check
    count_check = active_count + disposed_count + no_status_count
    value_check = active_value + disposed_value + no_status_value

    if count_check == total_assets and value_check == total_value:
        print("Control Check: OK")
    else:
        print("Control Check: ERROR")

    input("Press Enter to return to Report Menu...")

def department_summary():

    results = get_department_summary()

    print("\n--- Department-wise Asset Summary ---")
    print(f"{'Department':<20} {'Assets':>8} {'Value':>18}")
    print("-" * 48)

    total_count = 0
    total_value = 0

    for department, count, value in results:
        print(
            f"{department:<20} "
            f"{count:>8} "
            f"{value:>18,.2f}"
        )

        total_count += count
        total_value += value

    print("-" * 48)
    print(
        f"{'TOTAL':<20} "
        f"{total_count:>8} "
        f"{total_value:>18,.2f}"
    )

    if total_count == get_asset_count():
        print("Control Check: OK")
    else:
        print("Control Check: ERROR")

    input("\nPress Enter to return to Report Menu...")

def location_summary(assets):
    locations = {}

    for asset in assets:
        location = asset.get("location")

        if location is None or str(location).strip() == "":
            location = "None"

        value = asset.get("value") or 0

        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0

        if location not in locations:
            locations[location] = {
                "count": 0,
                "value": 0
            }

        locations[location]["count"] += 1
        locations[location]["value"] += value

    print("\n--- Location-wise Asset Summary ---")
    print(f"{'Location':<20} {'Assets':>8} {'Value':>18}")
    print("-" * 48)

    total_count = 0
    total_value = 0

    for location, data in locations.items():
        print(
            f"{location:<20} "
            f"{data['count']:>8} "
            f"{data['value']:>18,.2f}"
        )

        total_count += data["count"]
        total_value += data["value"]

    print("-" * 48)
    print(
        f"{'TOTAL':<20} "
        f"{total_count:>8} "
        f"{total_value:>18,.2f}"
    )

    if total_count == len(assets):
        print("Control Check: OK")
    else:
        print("Control Check: ERROR")

    input("\nPress Enter to return to Report Menu...")

def category_summary(assets):
    categories = {}

    for asset in assets:


        category = asset.get("category")

        if category is None or str(category).strip() == "":
            category = "None"
        else:
            category = str(category).strip().title()
        value = asset.get("value") or 0

        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0

        if category not in categories:
            categories[category] = {
                "count": 0,
                "value": 0
            }

        categories[category]["count"] += 1
        categories[category]["value"] += value

    print("\n--- Category-wise Asset Summary ---")
    print(f"{'Category':<20} {'Assets':>8} {'Value':>18}")
    print("-" * 48)

    total_count = 0
    total_value = 0

    for category, data in categories.items():
        print(
            f"{category:<20} "
            f"{data['count']:>8} "
            f"{data['value']:>18,.2f}"
        )

        total_count += data["count"]
        total_value += data["value"]

    print("-" * 48)
    print(
        f"{'TOTAL':<20} "
        f"{total_count:>8} "
        f"{total_value:>18,.2f}"
    )

    if total_count == len(assets):
        print("Control Check: OK")
    else:
        print("Control Check: ERROR")

    input("\nPress Enter to return to Report Menu...")

def status_summary(assets):
    statuses = {}

    for asset in assets:


        status = asset.get("status")

        if status is None or str(status).strip() == "":
            status = "None"
        else:
            status = str(status).strip().title()
        value = asset.get("value") or 0

        try:
            value = float(value)
        except (ValueError, TypeError):
            value = 0

        if status not in statuses:
            statuses[status] = {
                "count": 0,
                "value": 0
            }

        statuses[status]["count"] += 1
        statuses[status]["value"] += value

    print("\n--- Status-wise Asset Summary ---")
    print(f"{'Status':<20} {'Assets':>8} {'Value':>18}")
    print("-" * 48)

    total_count = 0
    total_value = 0

    for status, data in statuses.items():
        print(
            f"{status:<20} "
            f"{data['count']:>8} "
            f"{data['value']:>18,.2f}"
        )

        total_count += data["count"]
        total_value += data["value"]

    print("-" * 48)
    print(
        f"{'TOTAL':<20} "
        f"{total_count:>8} "
        f"{total_value:>18,.2f}"
    )

    if total_count == len(assets):
        print("Control Check: OK")
    else:
        print("Control Check: ERROR")

    input("\nPress Enter to return to Reports Menu...")

def reports_menu(assets):
    
    while True:
        print(f"\nTotal assets in database: {get_asset_count()}")
        print(f"Total asset value: {get_total_asset_value():,.2f}")
        print("\n--- Reports Menu ---")
        print("1. Overall Asset Summary")
        print("2. Department Summary")
        print("3. Location Summary")
        print("4. Category Summary")
        print("5. Status Summary")
        print("C. Return to Main Menu")

        choice = input("Enter your choice: ").strip().lower()

        if choice == "1":
            asset_summary(assets)

        elif choice == "2":
            department_summary()

        elif choice == "3":
            location_summary(assets)

        elif choice == "4":
            category_summary(assets)

        elif choice == "5":
            status_summary(assets)

        elif choice == "c":
            return

        else:
            print("Invalid choice.")



def main():
    create_database()
    while True:
        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
           db_assets = get_all_assets()
           add_asset(db_assets)
        

        elif choice == "2":
            db_assets = get_all_assets()
            list_assets(db_assets)


        elif choice == "3":
            db_assets = get_all_assets()
            edit_asset(db_assets)

        elif choice == "4":
            db_assets = get_all_assets()
            delete_asset(db_assets)

        elif choice == "5":
            db_assets = get_all_assets()
            search_asset(db_assets)

        elif choice == "6":
            db_assets = get_all_assets()
            filter_assets(db_assets)

        elif choice == "7":
            db_assets = get_all_assets()
            reports_menu(db_assets)

        elif choice == "8":
            print("Exiting program...")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()