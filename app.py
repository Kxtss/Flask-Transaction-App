# Import libraries
from flask import Flask, render_template, request, url_for, redirect

# Instantiate Flask functionality
app = Flask(__name__)

# Sample data
transactions = [
    {'id': 1, 'date': '2023-06-01', 'amount': 100},
    {'id': 2, 'date': '2023-06-02', 'amount': -200},
    {'id': 3, 'date': '2023-06-03', 'amount': 300}
]

# Read operation: List all transactions
@app.route("/")
def get_transactions():
    return render_template("transactions.html", transactions=transactions)

# Create operation: Display add transaction form
# Route to handle the creation of a new transaction
@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Create a new transaction object using form field values
        transaction = {
            'id': len(transactions) + 1,            # Generate a new ID based on the current length of the transactions list
            'date': request.form['date'],           # Get the 'date' field value from the form
            'amount': float(request.form['amount']) # Get the 'amount' field value from the form and convert it to a float
        }
        # Append the new transaction to the transactions list
        transactions.append(transaction)
        # Redirect to the transactions list page after adding the new transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, render the form template to display the add transaction form
    return render_template("form.html")

# Update operation: Display edit transaction form
# Route to handle the editing of an existing transaction
@app.route("/edit/<int:transaction_id>", methods=["GET", "POST"])
def edit_transaction(transaction_id):
    # Check if the request method is POST (form submission)
    if request.method == 'POST':
        # Extract the updated values from the form fields
        date = request.form['date']           # Get the 'date' field value from the form
        amount = float(request.form['amount'])# Get the 'amount' field value from the form and convert it to a float
        # Find the transaction with the matching ID and update its values
        for transaction in transactions:
            if transaction['id'] == transaction_id:
                transaction['date'] = date       # Update the 'date' field of the transaction
                transaction['amount'] = amount   # Update the 'amount' field of the transaction
                break                            # Exit the loop once the transaction is found and updated
        # Redirect to the transactions list page after updating the transaction
        return redirect(url_for("get_transactions"))
    
    # If the request method is GET, find the transaction with the matching ID and render the edit form
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            # Render the edit form template and pass the transaction to be edited
            return render_template("edit.html", transaction=transaction)
    # If the transaction with the specified ID is not found, handle this case (optional)
    return {"message": "Transaction not found"}, 404

# Delete operation: Delete a transaction
# Route to handle the deletion of an existing transaction
@app.route("/delete/<int:transaction_id>")
def delete_transaction(transaction_id):
    # Find the transaction with the matching ID and remove it from the list
    for transaction in transactions:
        if transaction['id'] == transaction_id:
            transactions.remove(transaction)  # Remove the transaction from the transactions list
            break  # Exit the loop once the transaction is found and removed
    # Redirect to the transactions list page after deleting the transaction
    return redirect(url_for("get_transactions"))

# Search operation: Search for transactions by amount range
# Route to handle the searching of transactions based on minimum and maximum amounts
@app.route('/search', methods=['GET', 'POST'])
def search_transactions():
    # Check if the request method is POST (form submission for search)
    if request.method == "POST":
        # Get the 'min_amount' and 'max_amount' values from the form.
        # Use .get() to safely retrieve values, returning None if not found.
        min_amount_str = request.form.get("min_amount")
        max_amount_str = request.form.get("max_amount")

        # Initialize min_amount and max_amount to None, indicating no specific limit
        min_amount = None
        max_amount = None

        # Attempt to convert string inputs to float.
        if min_amount_str:
            min_amount = float(min_amount_str)
        if max_amount_str:
            max_amount = float(max_amount_str)

        # Create an empty list to store the transactions that match the filter criteria
        filtered_transactions = []
        # Iterate over all transactions to apply the filter
        for transaction in transactions:
            # Ensure the 'amount' key exists and its value is a number (int or float)
            if "amount" in transaction and isinstance(transaction["amount"], (int, float)):
                amount = transaction["amount"]
                
                # Check if the transaction's amount falls within the specified range:
                # (min_amount is None OR amount is greater than or equal to min_amount)
                # AND
                # (max_amount is None OR amount is less than or equal to max_amount)
                if (min_amount is None or amount >= min_amount) and \
                   (max_amount is None or amount <= max_amount):
                    filtered_transactions.append(transaction) # Add transaction to the filtered list if it matches
        
        # Render the 'transactions.html' template, passing the filtered list of transactions.
        # Also pass the original min/max string values to pre-fill the search form if needed.
        return render_template("transactions.html", transactions=filtered_transactions,
                               min_amount_prev=min_amount_str, max_amount_prev=max_amount_str)
    
    # If the request method is GET, render the 'search.html' template to display the search form.
    return render_template("search.html")

# Balance operation: calculates and displays the total balance of all transactions
# Route to calculate and display the total balance of all transactions on the transactions page.
@app.route("/balance")
def total_balance():
    # Initialize the total balance to 0.0 to ensure correct accumulation.
    balance = 0.0
    
    # Iterate through each transaction in the global 'transactions' list.
    for transaction in transactions:
        # Check if the 'amount' key exists in the transaction and if its value is a number (int or float).
        if "amount" in transaction and isinstance(transaction["amount"], (int, float)):
            # Add the 'amount' of the current transaction to the running total balance.
            balance += transaction["amount"]
            
    # Return the total balance as a formatted string using an f-string.            
    return f"<p style='font-size: 3em; color: #333; text-align: center; margin-top: 50px;'>Balance Total: {balance:.2f}</p>"

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)