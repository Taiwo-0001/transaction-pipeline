from pathlib import Path

from flask import Flask, jsonify

from pipeline.processor import process_transactions


app = Flask(__name__)

PROJECT_ROOT = Path(__file__).resolve().parent
CSV_PATH = PROJECT_ROOT / "data" / "messy_transactions.csv"

processed_data = process_transactions(CSV_PATH)


@app.route("/transactions", methods=["GET"])
def get_transactions():
    """Return all valid transactions."""
    return jsonify(processed_data["transactions"])


@app.route("/transactions/<transaction_id>", methods=["GET"])
def get_transaction(transaction_id):
    """Return one transaction by ID."""
    for transaction in processed_data["transactions"]:
        if transaction["id"] == transaction_id:
            return jsonify(transaction)

    return jsonify({
        "error": "Transaction not found"
    }), 404


@app.route("/analytics/summary", methods=["GET"])
def get_summary():
    """Return the transaction summary."""
    return jsonify(processed_data["summary"])


@app.route("/analytics/categories", methods=["GET"])
def get_categories():
    """Return expenses grouped by category."""
    return jsonify(processed_data["expensesByCategory"])


if __name__ == "__main__":
    app.run(debug=True)