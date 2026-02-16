from flask import Flask, render_template_string, request,Blueprint
import pymysql
Brandlist = Blueprint("Brandlist",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@Brandlist.route('/brandlist', methods=['GET', 'POST'])
def Brandlist_index():
    brand_list = []


    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brand")
    brand_list = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Brand Management</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body>
  {% include 'navbar.html' %}
<h1>Brand Information</h1>

{% if brand_list %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Brand_Id</th>
        <th scope="row">Brand_Nm</th>
    </tr>
    </thead>
    <tbody>
    {% for row in brand_list %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,brand_list=brand_list)
