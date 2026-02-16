from flask import Flask, render_template_string, request,Blueprint
import pymysql
Customerlist = Blueprint('Customerlist',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')



@Customerlist.route('/customerlist', methods=['GET', 'POST'])
def Customerlist_index():
    custlist = []

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer")
    custlist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Customer</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body>
  {% include 'navbar.html' %}
<h1>Customer Info</h1>

{% if custlist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Cust_Id</th>
        <th scope="row">Cust_Nm</th>
        <th scope="row">Cust_Addr</th>
        <th scope="row">Cust_Phone</th>
        <th scope="row">Cust_Email</th>
        <th scope="row">Cust_Pincode</th>
        <th scope="row">Cust_Password</th>
    </tr>
    </thead>
    <tbody>
    {% for row in custlist %}
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
    return render_template_string(html_template,custlist=custlist)

