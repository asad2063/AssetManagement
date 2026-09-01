# ASSET MANAGEMENT SYSTEM
## Project Requirements and Design Decisions

**Document Version:** 1.0  
**Status:** Development  
**Purpose:** Master record of agreed system requirements and design decisions.

---

# 1. PURPOSE OF THIS DOCUMENT

This document records the agreed functional, accounting, validation, database,
migration, reporting and system design requirements for the Asset Management
System.

It shall be updated whenever an important design decision is made.

The objective is to ensure that program development remains consistent even
when development continues over a long period or is transferred to another
developer.

---

# 2. GENERAL DESIGN PRINCIPLE

Rules that may differ from one organization to another shall not be hard-coded
throughout the program.

Such rules shall be maintained centrally so that they can be changed without
rewriting multiple parts of the program.

Examples include:

- Date format
- Amount rounding/truncation policy
- Financial year
- Asset ID format
- Depreciation methods
- Depreciation rates
- Useful lives
- Asset categories
- Asset statuses
- Other organization-specific validation rules

---

# 3. CURRENT DEVELOPMENT STATUS

The system has progressed through:

1. Python fundamentals
2. Command-line Asset Management System
3. JSON data storage
4. SQLite database implementation
5. Add Asset
6. List Assets
7. Edit Asset
8. Delete Asset
9. Search Assets
10. Filter Assets
11. Basic reports

Current development focus:

- Finalization of asset master fields
- Database structure
- Accounting fields
- Depreciation requirements
- Validation rules

Future stages include:

- Depreciation and NBV module
- Enhanced reporting
- Legacy data migration from Excel
- Graphical User Interface (GUI)
- User authentication and authorization
- Audit trail
- Testing and production deployment

---

# 4. SYSTEM ASSET ID

The system shall automatically generate a unique Asset ID.

Example:

AST-0001
AST-0002
AST-0003

The system-generated Asset ID is separate from the physical Asset
Identification Code / Asset Tag.

---

# 5. ASSET IDENTIFICATION CODE

Database field:

asset_identification_code

The Asset Identification Code is NOT mandatory at initial entry or migration.

Where no identification code is available:

- The asset shall still be accepted into the system.
- The database should store NULL where appropriate.
- The user interface may display "Not provided".
- The asset shall appear in a separate exception/control report.

The system shall provide an:

"Assets Without Identification Codes" report.

This report is intended to assist management and auditors in identifying
assets that still require physical tagging/identification.

The report should eventually be available by:

- Department
- Location
- Asset category
- Original cost

The system should also be capable of reporting the percentage of assets for
which identification codes have been completed.

---

# 6. DATE POLICY

Current organization date format:

DD-MM-YYYY

Example of valid format:

01-12-2026

Example of invalid format:

1-12-2026

All date validation shall be controlled through a central date-validation
function/configuration.

Dates that represent historical transactions, such as acquisition dates,
shall not accept future dates.

Exceptions shall exist where a future date is logically valid.

Example:

Warranty End Date may be a future date.

Warranty End Date must not be earlier than the Acquisition Date.

The date format shall be configurable so that another organization may adopt
a different format without rewriting the program.

---

# 7. AMOUNT POLICY

Financial amounts shall be maintained in whole Rupees.

Decimal portions shall be TRUNCATED and NOT rounded.

Example:

133333.99 becomes 133,333

133333.50 becomes 133,333

4000000.75 becomes 4,000,000

All displayed financial amounts shall use comma separators.

Example:

4000000 becomes 4,000,000

The truncation/rounding policy shall be controlled centrally.

This is required so another organization may choose a different policy, such
as normal rounding, without changing calculations throughout the program.

---

# 8. CORE ASSET FIELDS

The asset master is expected to include, subject to further review:

## Identification and Classification

- System Asset ID
- Asset Identification Code / Asset Tag
- Asset Name / Description
- Category
- Sub-category
- Department
- Location
- Custodian / User
- Serial Number / Chassis Number / Equipment Number
- Manufacturer
- Model
- Status
- Physical Condition
- Remarks

## Accounting Information

- Asset GL Code
- Accumulated Depreciation GL Code
- Original Cost
- Accumulated Depreciation Amount
- Net Book Value (NBV)
- Residual / Scrap Value
- Capitalization Date
- Financial Year

## Acquisition Information

- Acquisition / Purchase Date
- Acquisition Method
- Supplier / Vendor
- Invoice Number
- Invoice Date
- Purchase Order / Work Order Number
- Quantity
- Warranty End Date

---

# 9. NET BOOK VALUE

NBV means Net Book Value.

The basic control formula is:

NBV = Original Cost - Accumulated Depreciation

NBV should normally be calculated by the system rather than manually entered.

For migrated historical records, an imported NBV may be used as a control
against the calculated NBV.

Any mismatch shall be reported before final migration.

---

# 10. DEPRECIATION

The system shall not be designed around only one depreciation method.

Supported methods should include at least:

- Straight Line
- Declining Balance

Additional methods may be added later.

Depreciation methods and rates may differ by asset category.

The design should therefore distinguish between:

Organization-wide rules

and

Asset-category-specific depreciation rules.

Possible depreciation fields include:

- Depreciation Method
- Depreciation Rate
- Useful Life
- Residual Value
- Depreciation Start Date
- Opening Accumulated Depreciation
- Opening NBV
- Opening Balance As-Of Date
- Current Period Depreciation
- Closing Accumulated Depreciation
- Closing NBV

Detailed depreciation calculation rules remain to be finalized.

---

# 11. ASSET STATUS AND PHYSICAL CONTROL

Possible controlled statuses include:

- Active
- Under Repair
- Idle
- Transferred
- Disposed
- Lost
- Written Off

Status values should eventually come from a controlled master list rather
than unrestricted user typing.

Physical verification fields may include:

- Last Verification Date
- Verification Status
- Physical Condition
- Custodian
- Location

---

# 12. DISPOSAL INFORMATION

For disposed assets, the system should eventually maintain:

- Disposal Date
- Disposal Method
- Sale Proceeds
- Disposal Approval / Reference
- NBV at Disposal
- Gain or Loss on Disposal
- Disposal Remarks

Basic control:

Gain / Loss on Disposal = Sale Proceeds - NBV at Disposal

Detailed disposal workflow will be developed later.

---

# 13. LEGACY DATA MIGRATION

Existing asset registers shall be capable of being migrated through a
standard Excel template.

The template shall clearly specify:

- Field name
- Mandatory / optional status
- Required data format
- Example
- Validation requirements

Migration shall be performed as at a specified migration/opening date.

The migration process should follow:

Existing Data
    ↓
Excel Migration Template
    ↓
Validation
    ↓
Staging / Preview
    ↓
Error Correction
    ↓
Approval
    ↓
Live Database

Data shall NOT be inserted directly into the permanent asset table without
validation.

Optional missing information may be displayed as:

Not provided

Where technically appropriate, missing numeric/date/database values should
be stored as NULL rather than storing the words "Not provided".

Mandatory missing fields shall prevent final import.

Incorrectly formatted data shall be identified separately.

The original incorrect value must NOT be destroyed.

Example:

Original Acquisition Date: 1-12-2026
Validation Result: Non compliant Format

A correctly formatted but prohibited future date should be separately
identified:

Validation Result: Future date not allowed

The migration process should produce a validation summary showing:

- Total records
- Records ready for import
- Records requiring correction
- Missing mandatory fields
- Invalid dates
- Invalid amounts
- Unknown categories
- Other validation errors

---

# 14. MIGRATION ACCOUNTING INFORMATION

For existing assets, migration should preserve sufficient opening accounting
information to establish the asset position at the migration date.

Important fields include:

- Original Cost
- Asset GL Code
- Accumulated Depreciation GL Code
- Opening Accumulated Depreciation
- Opening NBV
- Migration / Opening As-Of Date
- Legacy Asset ID, where available
- Migration Source
- Migration Batch
- Migration Notes

After the opening position has been accepted, the new system should take
responsibility for subsequent depreciation and asset movements.

---

# 15. CONTROLLED MASTER DATA

The final system should avoid uncontrolled variations such as:

Finance
FINANCE
Fin
Finance Dept
finance

Master tables/lists should eventually be considered for:

- Departments
- Locations
- Categories
- Sub-categories
- GL Accounts
- Asset Statuses
- Depreciation Methods

---

# 16. AUDIT TRAIL

The production system should eventually maintain information such as:

- Created At
- Created By
- Updated At
- Updated By
- Migration Source
- Migration Batch
- Record Status

Migrated historical assets should be distinguishable from assets entered
directly into the new system.

---

# 17. USER CONTROL AND AUTHORIZATION

The final production system is intended to support controlled user access.

The planned workflow includes segregation between:

- Data entry / input
- Review / authentication by an authorized manager

Detailed roles, permissions and approval workflow will be designed at a later
development stage.

---

# 18. FUTURE SYSTEM STRUCTURE

As the program grows, functionality should gradually be separated from
main.py.

Possible structure:

main.py
config.py
database.py
validators.py
calculations.py
reports.py

config.py
    Organization-specific rules and settings

validators.py
    Date validation
    Amount validation
    Code validation
    Other input validation

calculations.py
    Amount truncation/rounding
    Depreciation
    NBV
    Disposal gain/loss

database.py
    SQLite/database operations

reports.py
    Management, accounting and audit reports

The exact structure will be decided as development progresses.

---

# 19. DEVELOPMENT PRINCIPLE

Before adding a major field or function, consideration should be given to:

1. Is the field mandatory, optional, calculated, or optional-but-controlled?
2. What is its data type?
3. What validation applies?
4. Can it be missing in legacy data?
5. How will it be migrated?
6. Does it affect accounting calculations?
7. Does it require an exception/control report?
8. Is the rule organization-specific and therefore configurable?
9. Does it require an audit trail?
10. Will it require authorization or managerial approval?

## Version 1.1

Finalized Version 1 asset master design.

Added:

- Optional-but-controlled Asset Identification Code
- Custodian Master concept
- Custodian email and future reminder requirements
- Warranty End Date
- Centralized date and amount policies
- Truncation rather than rounding
- Configurable depreciation methods
- Relational database design principles


---

# 20. REQUIREMENTS CHANGE LOG

## Version 1.0

Initial requirements document created from the Asset Management System
development discussions.

Future agreed design changes should be added to this document and reflected
in the version/change history.