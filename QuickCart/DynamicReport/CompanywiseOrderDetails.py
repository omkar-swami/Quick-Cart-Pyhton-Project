from flask import Flask, render_template_string, request, Blueprint
import pymysql

CompanywiseOrderDetails = Blueprint('CompanywiseOrderDetails', __name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@CompanywiseOrderDetails.route('/CompanywiseOrderDetails', methods=['GET', 'POST'])
def CompanywiseOrderDetails_index():
    orderlist = []
    ordercomplist = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company")
    ordercomplist = cursor.fetchall()

    if request.method == 'POST':
        Comp_Id = request.form.get('Comp_Id')
        cursor.execute("SELECT Order_DetId,orderdetails.Order_Id,itemmaster.Item_Nm,Item_Qty,orderdetails.Item_Rate,Item_Amt,company.Comp_NM from orderdetails,itemmaster,company where orderdetails.Item_Id=itemmaster.Item_Id and company.Comp_Id=orderdetails.Comp_id and orderdetails.Comp_id=%s ",
                       (Comp_Id,))
        orderlist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OrderDetails</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

</head>
<body>
  {% include 'navbar.html' %}
<h1>OrderDetails Info</h1>
<form method="POST" action="/CompanywiseOrderDetails">


     <p>Select company </p>
    {% if ordercomplist %}
    <select class="form-control w-25" name="Comp_Id" id="txtOrderComp_Id">
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
        <th scope="row">Order Details Id </th>
        <th scope="row">Order Id</th>
        <th scope="row">Item Name</th>
        <th scope="row">Rate</th>
        <th scope="row">Qantity</th>
        <th scope="row">Total Amount</th>
        <th scope="row">Company Name</th>

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

