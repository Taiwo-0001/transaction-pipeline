import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pipeline.processor import parse_amount, parse_date, process_transactions


def test_amount():
    assert parse_amount("₦25,000") == 25000
    assert parse_amount("4,500") == 4500


def test_date():
    assert parse_date("2026-09-01") == "2026-09-01"
    assert parse_date("01/09/2026") == "2026-09-01"


def test_clean_data():
    result = process_transactions("data/clean_transactions.csv")

    assert result["summary"]["totalIncome"] == 220000
    assert result["summary"]["totalExpenses"] == 30000
    assert result["summary"]["balance"] == 190000
    assert result["summary"]["numberOfTransactions"] == 8


def test_messy_data():
    result = process_transactions("data/messy_transactions.csv")

    assert result["summary"]["totalIncome"] == 220000
    assert result["summary"]["totalExpenses"] == 9500
    assert result["summary"]["balance"] == 210500
    assert result["summary"]["numberOfTransactions"] == 6


def test_invalid_transactions():
    result = process_transactions("data/messy_transactions.csv")

    assert len(result["invalidTransactions"]) == 7

    reasons = [item["reason"] for item in result["invalidTransactions"]]

    assert "Missing description" in reasons
    assert "Invalid date format" in reasons
    assert "Missing category" in reasons
    assert "Amount must be greater than zero" in reasons
    assert "Amount must be numeric" in reasons
    assert "Type must be income or expense" in reasons