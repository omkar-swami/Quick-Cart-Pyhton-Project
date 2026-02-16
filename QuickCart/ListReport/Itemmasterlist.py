from flask import Flask, render_template_string, request,Blueprint
import pymysql
Itemmasterlist = Blueprint('Itemmasterlist',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')



@Itemmasterlist.route('/itemmasterlist', methods=['GET', 'POST'])
def Itemmasterlist_index():
    item_list = []

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itemmaster")
    Item_list = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Itemmaster</title>
    
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>
    
</head>
<body>
  {% include 'navbar.html' %}
<h1>Itemmaster Information</h1>

{% if Item_list %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Item_Id</th>
        <th scope="row">Item_Nm</th>
        <th scope="row">Comp_Id</th>
        <th scope="row">Cat_Id</th>
        <th scope="row">Brand_Id</th>
        <th scope="row">Item_Rate</th>
        <th scope="row">Item_Stock</th>
        <th scope="row">Item_Descr</th>
        <th scope="row">Item_Photo</th>
    </tr>
    </thead>
    <tbody>
    {% for row in Item_list %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>
        <td>{{ row[4] }}</td>
        <td>{{ row[5] }}</td>
        <td>{{ row[6] }}</td>
        <td>{{ row[7] }}</td>
        <td>{{ row[8] }}</td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>"""

    return render_template_string(html_template,Item_list=Item_list)


