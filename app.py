"""
Simple Transaction Management System

This Flask application manages financial transactions with CRUD operations,
search functionality, and balance calculation. It follows RESTful principles
and uses in-memory storage for demonstration purposes.

Features:
- List all transactions
- Add new transactions
- Edit existing transactions
- Delete transactions
- Search transactions by amount range
- Display total balance

Note: Data is stored in memory and resets on server restart.
"""

from flask import (
    Flask,
    render_template,
    redirect,
    request,
    url_for,
)  # pylint: disable=import-error

# Initialize Flask application
app = Flask(__name__)

# In-memory storage for transactions (temporary solution)
# In a production system, this would be replaced with a database
transactions = [
    {"id": 1, "date": "2023-06-01", "amount": 100},
    {"id": 2, "date": "2023-06-02", "amount": -200},
    {"id": 3, "date": "2023-06-03", "amount": 300},
]


@app.route("/")
def get_transactions():
    """Display all transactions.

    Renders the transactions template with the current list of transactions.

    Returns:
        Rendered HTML template with transactions data
    """
    return render_template("transactions.html", transactions=transactions)


@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    """Handle transaction creation.

    GET: Display transaction creation form
    POST: Process form submission and add new transaction

    Returns:
        Redirect to transactions list or form template
    """
    if request.method == "POST":
        # Create new transaction dictionary
        new_transaction = {
            "id": len(transactions) + 1,
            "date": request.form["date"],
            "amount": float(request.form["amount"]),
        }

        transactions.append(new_transaction)
        return redirect(url_for("get_transactions"))

    return render_template("form.html")


@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    """Handle transaction editing.

    Args:
        transaction_id: ID of transaction to edit

    Returns:
        Redirect to transactions list, edit form, or error message
    """
    if request.method == "POST":
        # Extract updated data from form
        updated_date = request.form["date"]
        updated_amount = float(request.form["amount"])

        # Find and update transaction
        for transaction in transactions:
            if transaction["id"] == transaction_id:
                transaction["date"] = updated_date
                transaction["amount"] = updated_amount
                return redirect(url_for("get_transactions"))

        return {"message": "Transaction not found"}, 404

    # Find transaction for editing
    for transaction in transactions:
        if transaction["id"] == transaction_id:
            return render_template("edit.html", transaction=transaction)

    return {"message": "Transaction not found"}, 404


@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    """Delete specified transaction.

    Args:
        transaction_id: ID of transaction to delete

    Returns:
        Redirect to transactions list
    """
    # Find and remove transaction without using global
    for i, transaction in enumerate(transactions):
        if transaction["id"] == transaction_id:
            del transactions[i]
            break

    return redirect(url_for("get_transactions"))


@app.route("/search", methods=["GET", "POST"])
def search_transactions():
    """Search transactions by amount range.

    GET: Display search form
    POST: Process search request and display results

    Returns:
        Rendered template with search results or error message
    """
    if request.method == "POST":
        try:
            min_val = float(request.form["min_amount"])
            max_val = float(request.form["max_amount"])

            if min_val > max_val:
                return "Invalid range: Minimum exceeds maximum", 400

            # Filter transactions within range
            results = [t for t in transactions if min_val <= t["amount"] <= max_val]

            return render_template("transactions.html", transactions=results)

        except (KeyError, ValueError):
            return "Invalid input values", 400

    return render_template("search.html")


@app.route("/balance")
def total_balance():
    """Calculate and display total balance.

    Returns:
        Rendered template with transactions and balance summary
    """
    total = sum(t["amount"] for t in transactions)
    balance_summary = f"Total Balance: {total:.2f}"

    return render_template(
        "transactions.html", transactions=transactions, total_balance=balance_summary
    )


if __name__ == "__main__":
    app.run(debug=True)
