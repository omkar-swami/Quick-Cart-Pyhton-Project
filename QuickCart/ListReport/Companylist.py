from flask import Flask, render_template_string, request,Blueprint
import pymysql
Companylist = Blueprint("Companylist",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@Companylist.route('/companylist', methods=['GET', 'POST'])
def Companylist_index():
    complist = []


    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM company")
    complist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Company</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body>
  {% include 'navbar.html' %}
<h1>Company Info</h1>

{% if complist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Comp_Id</th>
        <th scope="row">Comp_Nm</th>
        <th scope="row">Comp_Addr</th>
        <th scope="row">Comp_Phone</th>
        <th scope="row">Comp_Email</th>
        <th scope="row">Comp_City</th>
        <th scope="row">Comp_Descr</th>
        <th scope="row">Comp_Password</th>
    </tr>
    </thead>
    <tbody>
    {% for row in complist %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>
        <td>{{ row[4] }}</td>
        <td>{{ row[5] }}</td>
        <td>{{ row[6] }}</td>
        <td>{{ row[7] }}</td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,complist=complist)
