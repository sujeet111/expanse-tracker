from flask import Flask, request, render_template, redirect, url_for
from deta import Deta  # Import Deta
import json

deta = Deta()
income_db = deta.Base("income_db")
expense_db = deta.Base("expense_db")

app = Flask(__name__)

@app.route("/")
def index():
    total_expense=0
    fetch_data = expense_db.fetch({"expense_enabled": True})
    for i in fetch_data.items:
        total_expense += int(i['expense_value'])
    return render_template("index.html", data = {"items" :fetch_data.items,
                                                 'total_expense':total_expense})

@app.route("/create_expense", methods=["GET", "POST"])
def create_expense():
    if request.method == "POST":
        expense_name = request.form.get("expense_name")
        expense_value = request.form.get("expense_value")
        expense_monthly = request.form.get("expense_monthly")
        expense_daily = request.form.get("expense_daily")
        expense_date = request.form.get("expense_date")
        expense_type = request.form.get("expense_type")
        data = {'expense_name': expense_name,
                'expense_value': expense_value,
                'expense_monthly': expense_monthly,
                'expense_daily': expense_daily,
                'expense_date': expense_date,
                'expense_type': expense_type,
                'expense_enabled':True }
        expense_db.put(data)
        return redirect(url_for('root'))
    return render_template("create_expense.html")

@app.route("/update/<string:id>", methods=["GET", "POST"])
def update_expense(id):
    try:
        if request.method == "GET":
            fetch_data = expense_db.get(id)
            print(type(fetch_data))
            fetch_data.pop("key")
            fetch_data = json.dumps(fetch_data, indent=4)
            return render_template("update.html", fetch_data=fetch_data, key=id)
        if request.method == "POST":
            key = request.form.get("expense_key")
            expense_data = eval(request.form.get("expense_update"))
            expense_db.update(expense_data, key)
            return redirect(url_for('root'))
    except Exception as e:
        # Handle the exception here
        print("An error occurred:", str(e))
        # Return an error message or redirect to an error page
        return "An error occurred: " + str(e)

@app.route("/delete/<string:id>", methods=["GET", "POST"])
def delete_expense(id):
    try:
        if request.method == "GET":
            fetch_data = expense_db.get(id)
            print(type(fetch_data))
            fetch_data.pop("key")
            fetch_data = json.dumps(fetch_data, indent=4)

            return render_template("delete.html", fetch_data=fetch_data, key=id)
        if request.method == "POST":
            key = request.form.get("expense_key")
            expense_data = eval(request.form.get("expense_update"))
            expense_data["expense_enabled"] = False
            expense_db.delete(expense_data, key)
            return redirect(url_for('index'))
    except Exception as e:
        # Handle the exception here
        print("An error occurred:", str(e))
        # Return an error message or redirect to an error page
        return "An error occurred: " + str(e)
    
@app.route("/create_income", methods=["GET", "POST"])
def create_income():
    if request.method == "POST":
        income_name = request.form.get("income_name")
        income_value = request.form.get("income_value")
        income_monthly = request.form.get("income_monthly")
        income_daily = request.form.get("income_daily")
        income_date = request.form.get("income_date")
        income_type = request.form.get("income_type")
        data = {'income_name': income_name,
                'income_value': income_value,
                'income_monthly': income_monthly,
                'income_daily': income_daily,
                'income_date': income_date,
                'income_type': income_type,
                'income_enabled':True }
        income_db.put(data)
        return redirect(url_for('root'))
    return render_template("create_income.html")

if __name__ == '__main__':
    app.run(debug=True, port=5001)
