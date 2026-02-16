from flask import Flask, render_template_string, request,Blueprint
import pymysql
OrderMasterwisePayment = Blueprint('OrderMasterwisePayment',__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@OrderMasterwisePayment.route('/ordermasterwisepayment', methods=['GET', 'POST'])
def OrderMasterwisePayment_index():
    paylist = []
    orderlist = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordermaster")
    orderlist = cursor.fetchall()

    if request.method == 'POST':
        Order_date = request.form['Order_date']
        cursor.execute("SELECT * FROM payment WHERE Pay_Date= %s", (Order_date))
        paylist = cursor.fetchall()
        cursor.close()
        conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>payment</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body>
  {% include 'navbar.html' %}
<h1>Day Wise Payment</h1>
<form method="POST" action="/ordermasterwisepayment">

    <p>Select Date</p>
    {% if orderlist %}
    <select class="form-control w-25" name="Order_date" id="txtOrder_Id">
        {% for data in orderlist %}
        <option value="{{data[1]}}">{{data[1]}}</option>
        {% endfor %}
    </select>
    {% endif %}

    <input type="submit" value="show"  name="btn" class="btn btn-secondary btn-sm"/><br><br>
</form>

{% if paylist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Pay_Id</th>
        <th scope="row">Pay_Date</th>
        <th scope="row">Order_Id</th>
        <th scope="row">Order_GrandTot</th>

    </tr>
    </thead>
    <tbody>
    {% for row in paylist %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>

    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  paylist=paylist,
                                  orderlist=orderlist
                                  )

