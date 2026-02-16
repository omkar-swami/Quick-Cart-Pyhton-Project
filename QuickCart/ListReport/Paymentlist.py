from flask import Flask, render_template_string, request, Blueprint
import pymysql
Paymentlist = Blueprint('Paymentlist',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')



@Paymentlist.route('/paymentlist', methods=['GET', 'POST'])
def Paymentlist_index():
    paylist = []

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payment")
    paylist = cursor.fetchall()
    cursor.execute("SELECT * FROM ordermaster")
    orderlist = cursor.fetchall()
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
<h1>Payment Information</h1>

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
    return render_template_string(html_template,paylist=paylist)

