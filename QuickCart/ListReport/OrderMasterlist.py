from flask import Flask, render_template_string, request, Blueprint
import pymysql
OrderMasterlist = Blueprint('OrderMasterlist',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@OrderMasterlist.route('/ordermasterlist', methods=['GET', 'POST'])
def OrderMasterlist_index():
    orderlist = []

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordermaster")
    orderlist = cursor.fetchall()
    cursor.execute("SELECT * FROM customer")
    ordercustlist = cursor.fetchall()
    cursor.execute("SELECT * FROM company")
    ordercomplist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ordermaster</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body style="margin-top:100px">
  {% include 'navbar.html' %}
<h1>OrderMaster Info</h1>

{% if orderlist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Order_Id</th>
        <th scope="row">Order_Date</th>
        <th scope="row">OrderCust_Id</th>
        <th scope="row">Order_Amt</th>
        <th scope="row">Order_GSTAmt</th>
        <th scope="row">Order_GrandTot</th>
    </tr>
    </thead>
    <tbody>
    {% for row in orderlist %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>
        <td>{{ row[4] }}</td>
        <td>{{ row[5] }}</td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,orderlist=orderlist,)
