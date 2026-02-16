from flask import Flask, render_template_string, request,Blueprint
import pymysql
Itemcategory = Blueprint("Itemcategory",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid=0
    qry="SELECT MAX(Cat_Id) FROM itemcat"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid=i[0]
        if maxid is None:
            maxid="0"
        return int(maxid) + 1

def clear_textbox():
    return '', ''

@Itemcategory.route('/itemcat', methods=['GET', 'POST'])
def Itemcategory_index():
    catlist = []
    Cat_Id = ''
    Cat_Nm = ''
    Cat_Id = request.args.get('Cat_Id', '')
    Cat_Nm = request.args.get('Cat_Nm', '')
    is_record = bool(Cat_Id)

    if not is_record:
        Cat_Id = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Cat_Id = request.form['Cat_Id']
            Cat_Nm = request.form['Cat_Nm']

            if btn == 'Insert':
                cursor.execute("INSERT INTO itemcat VALUES (%s, %s)", (Cat_Id, Cat_Nm))
                conn.commit()
                Cat_Id, Cat_Nm = clear_textbox()
                Cat_Id = GetNewID()
                is_record = False
            elif btn == 'Update':
                cursor.execute("UPDATE itemcat SET Cat_Nm=%s WHERE Cat_Id=%s", (Cat_Nm, Cat_Id))
                conn.commit()
                Cat_Id, Cat_Nm = clear_textbox()
                Cat_Id = GetNewID()
                is_record = False
            elif btn == 'Delete':
                cursor.execute("DELETE FROM itemcat WHERE Cat_Id=%s", (Cat_Id,))
                conn.commit()
                Cat_Id, Cat_Nm = clear_textbox()
                Cat_Id = GetNewID()
                is_record = False
        except Exception as e:
            print (e)


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
    
    <script>
                    function formValidator() {            
                        var Cat_Id = document.getElementById("txtCat_Id");
                        var Cat_Nm = document.getElementById("txtCat_Nm");
                          
                                    
                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Cat_Nm, "Name Must be given") && isAlphabet(Cat_Nm, "Please enter only letters for your name")) {
                                                return true;  
                        }                                           
                     return false;
                    }
                </script>
                <script src="{{url_for('static',filename='js/ValidationLibrary.js')}}"></script>
                
                <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
                <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

    
</head>
<body>
  {% include 'navbar.html' %}
<h1>Item Category Information</h1>
<form method="POST" action="/itemcat">
    <p>Enter Category ID:</p>
    <input type="text" class="form-control w-25" name="Cat_Id" value="{{ Cat_Id }}"/>
    <p>Enter Category Name:</p>
    <input type="text" class="form-control w-25" name="Cat_Nm" id="txtCat_Nm" value="{{ Cat_Nm }}"/><br><br>
    
    <input type="submit" value="Insert" {% if is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-primary"/>
    <input type="submit" value="Update" {% if not is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-success"/>
    <input type="submit" value="Delete" {% if not is_record %} disabled {% endif %} name="btn" class="btn btn-danger"/><br><br>
</form>
{% if catlist %}
<table border="2px" class="table table-hover">
    <thead>
    <tr>
        <th scope="row">Cat_Id</th>
        <th scope="row">Cat_Nm</th>
        <th scope="row">Select</th>
    </tr>
    </thead>
    <tbody>
    {% for row in catlist %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td><a href="/itemcat?Cat_Id={{ row[0] }}&Cat_Nm={{ row[1] }}" class="btn btn-outline-info">select</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  catlist=catlist,
                                  Cat_Id=Cat_Id,
                                  Cat_Nm=Cat_Nm,
                                  is_record=is_record)

