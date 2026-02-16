from flask import Flask, render_template_string, request,Blueprint
import pymysql
Orderdetailslist = Blueprint('Orderdetailslist',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@Orderdetailslist.route('/orderdetailslist', methods=['GET', 'POST'])
def Orderdetailslist_index():
    orderDetlist = []


    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Order_DetId,orderdetails.Order_Id,itemmaster.Item_Nm,Item_Qty,orderdetails.Item_Rate,Item_Amt,company.Comp_NM from orderdetails,itemmaster,company where orderdetails.Item_Id=itemmaster.Item_Id and company.Comp_Id=orderdetails.Comp_id")
    orderDetlist = cursor.fetchall()
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
<h1>OrderDetails</h1>
</form>

{% if orderDetlist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Order_DetId</th>
        <th scope="row">Order_Id</th>
        <th scope="row">Item_Id</th>
        <th scope="row">Item_Rate</th>
        <th scope="row">Item_Qyt</th>
        <th scope="row">Item_Amt</th>
        <th scope="row">Company Name</th>
    </tr>
    </thead>
    <tbody>
    {% for row in orderDetlist %}
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
    return render_template_string(html_template,orderDetlist=orderDetlist)
