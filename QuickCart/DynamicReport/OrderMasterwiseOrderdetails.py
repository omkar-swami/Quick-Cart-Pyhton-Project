from flask import Flask, render_template_string, request,Blueprint
import pymysql

OrderMasterwiseOrderdetails = Blueprint('OrderMasterwiseOrderdetails',__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

@OrderMasterwiseOrderdetails.route('/ordermasterwiseOrderDetails', methods=['GET', 'POST'])
def OrderMasterwiseOrderdetails_index():
    orderdetlist = []
    orderlist = []
    itemlist = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordermaster")
    orderlist = cursor.fetchall()

    if request.method == 'POST':
        Order_Id = request.form.get('Order_Id')
        cursor.execute("SELECT * FROM orderdetails where Order_Id=%s ", (Order_Id,))
        orderdetlist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>orderdetails</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body>
  {% include 'navbar.html' %}
<h1>OrderDetails</h1>
<form method="POST" action="/ordermasterwiseOrderDetails">

    <p>Select OrderMaster</p>
    {% if orderlist %}
    <select class="form-control w-25" name="Order_Id" id="txtOrder_Id">
    {% for data in orderlist %}
    <option value="{{data[0]}}">{{data[1]}}</option>
    {% endfor %}
    </select>
    {% endif %}

    <input type="submit" value="show" name="btn"/ class="btn btn-secondary btn-sm"><br><br>
</form>
{% if orderdetlist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Order_DetId</th>
        <th scope="row">Order_Id</th>
        <th scope="row">Item_Id</th>
        <th scope="row">Item_Rate</th>
        <th scope="row">Item_Qyt</th>
        <th scope="row">Item_Amt</th>
    </tr>
    </thead>
    <tbody>
    {% for row in orderdetlist %}
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
    return render_template_string(html_template,
                                  orderdetlist=orderdetlist,
                                  orderlist=orderlist,
                                  itemlist=itemlist,
                                  )


