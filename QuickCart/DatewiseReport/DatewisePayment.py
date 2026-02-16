from flask import Flask, render_template_string, request,Blueprint
import pymysql

DatewisePayment = Blueprint('DatewisePayment',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

@DatewisePayment.route('/datewisePayment', methods=['GET', 'POST'])
def DatewisePayment_index():
    paylist = []

    if request.method == 'POST':
        fromdate = request.form.get('b1')
        todate = request.form.get('b2')
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM payment WHERE Pay_Date BETWEEN %s AND %s",
                       (fromdate, todate))
        paylist = cursor.fetchall()
        cursor.close()
        conn.close()


    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>payment</title>
</head>

<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
<script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

<body>
  {% include 'navbar.html' %}
<h1>Payment Information</h1>
<form method="POST" action="/datewisePayment">
    <p>Enter fromdate:</p>
   <input type="date" class="form-control w-25" name="b1"/>
    <p>Enter todate:</p>
    <input type="date" class="form-control w-25" name="b2"/>
    <input type="submit" value="show" class="btn btn-secondary btn-sm"/>
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
                                  paylist=paylist)

