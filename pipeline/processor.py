import csv
import json
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path


REQUIRED_FIELDS = [
    "id",
    "date",
    "description",
    "amount",
    "type",
    "category",
]

VALID_TYPES = {"income", "expense"}


def clean_text(value):
    """Remove unnecessary whitespace from text."""
    return str(value or "").strip()


def parse_date(value):
    """Convert accepted date formats to YYYY-MM-DD."""
    value = clean_text(value)

    formats = ["%Y-%m-%d", "%d/%m/%Y"]

    for date_format in formats:
        try:
            return datetime.strptime(value, date_format).strftime(
                "%Y-%m-%d"
            )
        except ValueError:
            continue

    raise ValueError("Invalid date format")

def parse_amount(value):
    """Convert amounts such as ₦25,000 or 4,500 to naira."""
    value = clean_text(value)

    if not value:
        raise ValueError("Amount is missing")

    cleaned = re.sub(r"[₦$€£,\s]", "", value)

    try:
        amount = Decimal(cleaned)
    except InvalidOperation:
        raise ValueError("Amount must be numeric")

    if not amount.is_finite():
        raise ValueError("Amount must be finite")

    if amount <= 0:
        raise ValueError("Amount must be greater than zero")

    if amount != amount.to_integral_value():
        raise ValueError("Amount must be a whole number of naira")

    return int(amount)

def validate_and_clean(row):
    """Clean one row and return a valid transaction or an error."""
    for field in REQUIRED_FIELDS:
        if field not in row:
            return None, f"Missing field: {field}"

    transaction = {
        field: clean_text(row[field])
        for field in REQUIRED_FIELDS
    }

    if not transaction["id"]:
        return None, "Missing transaction ID"

    if not transaction["description"]:
        return None, "Missing description"

    if not transaction["category"]:
        return None, "Missing category"

    try:
        transaction["date"] = parse_date(transaction["date"])
        transaction["amount"] = parse_amount(transaction["amount"])
    except ValueError as error:
        return None, str(error)

    transaction["type"] = transaction["type"].lower()

    if transaction["type"] not in VALID_TYPES:
        return None, "Type must be income or expense"

    return transaction, None


def process_transactions(csv_path):
    """Read, validate, clean, and summarize transactions."""
    valid_transactions = []
    invalid_transactions = []
    seen_ids = set()

    with open(csv_path, "r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        for row_number, row in enumerate(reader, start=2):
            transaction_id = clean_text(row.get("id", ""))

            if transaction_id in seen_ids:
                invalid_transactions.append({
                    "row": row_number,
                    "id": transaction_id,
                    "reason": "Duplicate transaction ID",
                    "data": row,
                })
                continue

            transaction, error = validate_and_clean(row)

            if error:
                invalid_transactions.append({
                    "row": row_number,
                    "id": transaction_id,
                    "reason": error,
                    "data": row,
                })
                continue

            seen_ids.add(transaction["id"])
            valid_transactions.append(transaction)

    total_income = sum(
        transaction["amount"]
        for transaction in valid_transactions
        if transaction["type"] == "income"
    )

    total_expenses = sum(
        transaction["amount"]
        for transaction in valid_transactions
        if transaction["type"] == "expense"
    )

    expenses_by_category = {}

    for transaction in valid_transactions:
        if transaction["type"] == "expense":
            category = transaction["category"]
            expenses_by_category[category] = (
                expenses_by_category.get(category, 0)
                + transaction["amount"]
            )

    result = {
        "summary": {
            "totalIncome": total_income,
            "totalExpenses": total_expenses,
            "balance": total_income - total_expenses,
            "numberOfTransactions": len(valid_transactions),
        },
        "expensesByCategory": expenses_by_category,
        "transactions": valid_transactions,
        "invalidTransactions": invalid_transactions,
        "transactionsProcessed": len(valid_transactions),
    }

    return result


def save_json(data, output_path):
    """Save processed results to a JSON file."""
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    project_root = Path(__file__).resolve().parent.parent
    csv_path = project_root / "data" / "messy_transactions.csv"
    output_path = project_root / "output.json"

    result = process_transactions(csv_path)
    save_json(result, output_path)

    print(json.dumps(result, indent=2, ensure_ascii=False))