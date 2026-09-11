
## How to Run the Project

First, open the project folder in VS Code.

Open the terminal and activate the virtual environment using:
venv\Scripts\activate


Install the required packages:


Run the data pipeline using:

python pipeline/processor.py

This will read the CSV file, clean the data and create and update the output.json file.

To run the API use:

python app.py



To run the tests, open another terminal and run:

pytest


The tests should show:

5 passed


## Project Structure


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
├── requirements.txt
└── README.md


## Data Validation Rules

The following fields are required:

* id
* date
* description
* amount
* type
* category

The validation rules I used are:

1. The transaction must have an ID.
2. The description cannot be empty.
3. The category cannot be empty.
4. The date must be in a valid format.
5. The amount must be a number.
6. The amount must be greater than zero.
7. The type must be either income or expense.
8. Duplicate transaction IDs are rejected.

## How I Handled Bad Data

When a transaction is not valid, I do not include it in the calculations.

Instead, I put it inside invalidTransactions and save the reason why it was rejected.

For example, if the amount is abc, the transaction is rejected because the amount is not a number.

This helps me know which records were bad and why they were not used.



## Clean Dataset Result

For the clean dataset, the program gives:


Total income: ₦220,000
Total expenses: ₦30,000
Balance: ₦190,000
Number of transactions: 8


There is a small difference between this result and the expected result stated in the test.

The test says the total expenses should be ₦30,500 and the balance should be ₦189,500.

However, when I checked the actual clean CSV file, the expense values add up to ₦30,000.

Therefore, I used the result from the actual data instead of changing the code to give the expected result.

## Messy Dataset Result

After cleaning the messy dataset, the result is:

Total income: ₦220,000
Total expenses: ₦9,500
Balance: ₦210,500
Number of valid transactions: 6


There were also 7 invalid transactions.

Some of the reasons were:

* Missing description
* Invalid date
* Missing category
* Amount is zero
* Amount is not a number
* Invalid transaction type

## API

I used Flask to create the API.

The API has these endpoints:

### Get all transactions

GET /transactions


This returns all the valid transactions.

### Get one transaction

GET /transactions/txn_101
This returns the transaction with that ID.

If the transaction does not exist, the API returns `404`.

### Get summary


GET /analytics/summary


This gives the total income, total expenses, balance and number of transactions.

### Get expenses by category


GET /analytics/categories


This shows how much was spent under each expense category.

## Testing

I used Pytest to test some important parts of the program.

The tests check things like:

* Amount cleaning
* Date conversion
* Clean data results
* Messy data results
* Invalid transactions

I ran:

pytest


The result was:

5 passed


## Assumptions

Some assumptions I made are:

* Every transaction should have a unique ID.
* Amounts are in Nigerian naira.
* Amounts must be greater than zero.
* A transaction must have a category.
* Only income and expense are accepted as transaction types.
* The accepted date formats are YYYY-MM-DD and DD/MM/YYYY.

## What I Would Improve

If I had more time, I would improve the project by:

* Adding more tests
* Adding better error messages
