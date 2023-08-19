from flask import Flask, request, render_template, redirect, url_for
from deta import Deta  # Import Deta
import json

deta = Deta()
income_db = deta.Base("income_db")
expense_db = deta.Base("expense_db")
db_mapping = {
    "expense": expense_db,
    "income": income_db
}


app = Flask(__name__)

@app.route("/")
def index():
    total_expense=0
    total_income=0
    expense_fetch_data = expense_db.fetch({"enabled": True})
    income_fetch_data = income_db.fetch({"enabled": True})

    for i in expense_fetch_data.items:total_expense += int(i['value'])
    for i in income_fetch_data.items:total_income += int(i['value'])

    return render_template("index.html", data = {"expense_fetch_data": expense_fetch_data.items,
                                                 "income_fetch_data": income_fetch_data.items,
                                                 'total_expense':total_expense,
                                                 "total_income":total_income})

@app.route("/create/<string:action_type>", methods=["GET", "POST"])
def create(action_type):
    if request.method == "POST":
        data_keys = ['name', 'value', 'monthly', 'daily', 'date', 'type']
        data = {key: request.form.get(key) for key in data_keys}
        data['enabled'] = True
        if action_type == 'expense':
            expense_db.put(data) 
        elif action_type == 'income':
            income_db.put(data)
        return redirect(url_for('index'))
    return render_template("create.html",task='create_expense')


@app.route("/modify/<string:category>/<string:action_type>/<string:id>", methods=["GET", "POST"])
def modify(category,action_type,id):
    db = db_mapping.get(category)

    try:
        if request.method == "GET":
            fetch_data = db.get(id)
            fetch_data.pop("key")
            fetch_data.pop("enabled")
            fetch_data = json.dumps(fetch_data, indent=4)
            return render_template("modify.html", fetch_data=fetch_data, key=id)
        if request.method == "POST":
            key = request.form.get("key")
            form_data = eval(request.form.get("NewData"))
            if action_type == "delete":
                form_data['enabled'] = False
            else:
                raise Exception('Invalid Operation')
            db.update(form_data, key)

            return redirect(url_for('index'))
    except Exception as e:
        return "An error occurred: " + str(e)

@app.route("/delete/<string:id>", methods=["GET", "POST"])
def delete_expense(id):
    try:
        if request.method == "GET":
            fetch_data = expense_db.get(id)
            print(type(fetch_data))
            fetch_data.pop("key")
            fetch_data = json.dumps(fetch_data, indent=4)

            return render_template("modify.html", fetch_data=fetch_data, key=id)
        if request.method == "POST":
            key = request.form.get("key")
            expense_data = eval(request.form.get("update"))
            expense_data["enabled"] = False
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
        name = request.form.get("name")
        value = request.form.get("value")
        monthly = request.form.get("monthly")
        daily = request.form.get("daily")
        date = request.form.get("date")
        type = request.form.get("type")
        data = {'name': name,
                'value': value,
                'monthly': monthly,
                'daily': daily,
                'date': date,
                'type': type,
                'enabled':True }
        income_db.put(data)
        return redirect(url_for('root'))
    return render_template("create_income.html",task='create_income')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
