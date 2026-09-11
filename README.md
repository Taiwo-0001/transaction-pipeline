# Transaction Data Processing Pipeline

## Overview

This project implements a Python-based transaction data processing pipeline. It reads transaction data from CSV files, validates and cleans the records, separates valid and invalid transactions, calculates financial summaries, and provides the processed data through a REST API built with Flask.

The pipeline is designed to handle both clean and messy transaction datasets.

---

## Project Structure

```text
transaction-pipeline/

│
├── data/
│   ├── clean_transactions.csv
│   └── messy_transactions.csv
│
├── pipeline/
│   ├── __init__.py
│   └── processor.py
│
├── tests/
│   └── test_processor.py
│
├── app.py
├── output.json
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Technologies Used

* Python
* Flask
* CSV
* JSON
* Regular Expressions
* Decimal
* Pytest

---

## Features

The pipeline performs the following tasks:

* Reads transaction data from CSV files.
* Validates required transaction fields.
* Cleans unnecessary whitespace.
* Converts different date formats to `YYYY-MM-DD`.
* Removes currency symbols and commas from monetary values.
* Validates transaction amounts.
* Validates transaction types.
* Detects invalid transactions.
* Detects duplicate transaction IDs.
* Calculates total income.
* Calculates total expenses.
* Calculates account balance.
* Groups expenses by category.
* Provides transaction data through REST API endpoints.

---

## Data Validation and Cleaning Rules

The following fields are required:

* ID
* Date
* Description
* Amount
* Type
* Category

### Date

The pipeline accepts:

```text
YYYY-MM-DD
DD/MM/YYYY
```

Dates are converted to:

```text
YYYY-MM-DD
```

### Amount

The pipeline removes:

* Currency symbols such as `₦`, `$`, `€`, and `£`
* Commas
* Extra spaces

For example:

```text
₦25,000
```

is converted to:

```text
25000
```

Amounts must be numeric, positive, finite, and expressed as whole naira values.

### Transaction Type

Only the following transaction types are accepted:

```text
income
expense
```

Transaction types are converted to lowercase before validation.

### Invalid Transactions

A transaction is rejected if it contains issues such as:

* Missing transaction ID
* Missing description
* Missing category
* Invalid date
* Invalid amount
* Negative or zero amount
* Invalid transaction type
* Duplicate transaction ID

Invalid records are preserved in the output together with the reason they were rejected.

---

## Running the Data Pipeline

Make sure the virtual environment is activated.

Run:

```bash
python pipeline/processor.py
```

The processed result is displayed in the terminal and saved to:

```text
output.json
```

---

## Clean Dataset Result

When the supplied clean dataset is processed, the pipeline produces:

```json
{
  "totalIncome": 220000,
  "totalExpenses": 30000,
  "balance": 190000,
  "numberOfTransactions": 8
}
```

### Note on the Expected Result

There is a discrepancy between the expected result stated in the assignment and the actual values contained in the supplied clean dataset.

The assignment states an expected total expense of:

```text
₦30,500
```

and an expected balance of:

```text
₦189,500
```

However, the four expense records in the supplied clean dataset are:

```text
₦5,000
₦4,500
₦12,000
₦8,500
```

These add up to:

```text
₦30,000
```

Therefore, based on the actual data provided, the correct calculated balance is:

```text
₦220,000 - ₦30,000 = ₦190,000
```

The pipeline therefore reports **₦30,000 total expenses and ₦190,000 balance** rather than the assignment's stated ₦30,500 and ₦189,500.

The code was not modified to artificially produce the stated expected result because doing so would make the calculation inconsistent with the supplied dataset.

---

## Messy Dataset Result

The messy dataset is also processed by the same validation and cleaning pipeline.

The resulting summary is:

```json
{
  "totalIncome": 220000,
  "totalExpenses": 9500,
  "balance": 210500,
  "numberOfTransactions": 6
}
```

Six transactions are accepted as valid, while **seven transactions are rejected** because of validation errors.

---

## REST API

The project includes a Flask REST API.

Start the API with:

```bash
python app.py
```

The API runs locally at:

```text
http://127.0.0.1:5000
```

### Get All Transactions

```http
GET /transactions
```

Example:

```text
http://127.0.0.1:5000/transactions
```

Returns all valid transactions.

### Get Transaction by ID

```http
GET /transactions/<id>
```

Example:

```text
http://127.0.0.1:5000/transactions/txn_101
```

If the transaction does not exist, the API returns a `404` response.

### Get Summary

```http
GET /analytics/summary
```

Example:

```text
http://127.0.0.1:5000/analytics/summary
```

Returns:

* Total income
* Total expenses
* Balance
* Number of valid transactions

### Get Expenses by Category

```http
GET /analytics/categories
```

Example:

```text
http://127.0.0.1:5000/analytics/categories
```

Returns total expenses grouped by category.

---

## Installation

Clone or download the project and navigate to the project directory.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

---

## Testing

Automated tests are included in the `tests` directory.

Run the tests using:

```bash
pytest
```

The tests verify important pipeline functions including data validation, amount parsing, date parsing, and tr
