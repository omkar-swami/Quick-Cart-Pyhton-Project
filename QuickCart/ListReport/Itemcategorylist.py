from flask import Flask, render_template_string, request,Blueprint
import pymysql
Itemcategorylist = Blueprint('Itemcategorylist',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@Itemcategorylist.route('/itemcatlist', methods=['GET', 'POST'])
def Itemcategorylist_index():
    catlist = []


    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itemcat")
    catlist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Item Category</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body>
  {% include 'navbar.html' %}
<h1>Item Category Information</h1>
    
    {% if catlist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Cat_Id</th>
        <th scope="row">Cat_Nm</th>
    </tr>
    </thead>
    <tbody>
    {% for row in catlist %}
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
    return render_template_string(html_template,catlist=catlist)
