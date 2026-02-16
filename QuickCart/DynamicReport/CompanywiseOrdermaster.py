from flask import Flask, render_template_string, request,Blueprint
import pymysql

CompanywiseOrdermaster = Blueprint('CompanywiseOrdermaster',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@CompanywiseOrdermaster.route('/companywiseordermaster', methods=['GET', 'POST'])
def CompanywiseOrdermaster_index():
    orderlist = []
    ordercomplist = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company")
    ordercomplist = cursor.fetchall()

    if request.method == 'POST':
        OrderComp_Id = request.form.get('OrderComp_Id')
        cursor.execute("SELECT * FROM ordermaster WHERE  OrderComp_Id = %s",
                       (OrderComp_Id,))
        orderlist = cursor.fetchall()
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
<body>
  {% include 'navbar.html' %}
<h1>ordermaster Info</h1>
<form method="POST" action="/companywiseordermaster">


     <p>Select company </p>
    {% if ordercomplist %}
    <select class="form-control w-25" name="OrderComp_Id" id="txtOrderComp_Id">
        {% for data in ordercomplist %}
        <option value="{{data[0]}}">{{data[1]}}</option>
        {% endfor %}
    </select>
    {% endif %}


    <input type="submit" value="show"  value="btn" class="btn btn-secondary btn-sm"/><br><br>
</form>
{% if orderlist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Order_Id</th>
        <th scope="row">Order_Date</th>
        <th scope="row">OrderCust_Id</th>
        <th scope="row">OrderComp_Id</th>
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
        <td>{{ row[6] }}</td>

    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template, orderlist=orderlist,
                                  ordercomplist=ordercomplist)

