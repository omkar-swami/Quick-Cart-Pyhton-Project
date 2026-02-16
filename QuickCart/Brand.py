from flask import Flask, render_template_string, request,Blueprint
import pymysql
Brand=Blueprint("Brand",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid=0
    qry="SELECT MAX(Brand_Id) FROM brand"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid=i[0]
        if maxid is None:
            maxid="0"
        return int(maxid) + 1

def clear_textbox():
    return '', ''

@Brand.route('/brand', methods=['GET', 'POST'])
def Brand_index():
    brand_list = []
    Brand_Id=''
    Brand_Nm=''
    Brand_Id=request.args.get('Brand_Id','')
    Brand_Nm= request.args.get('Brand_Nm', '')
    is_record = bool(Brand_Id)

    if not is_record:
        Brand_Id = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Brand_Id = request.form['Brand_Id']
            Brand_Nm = request.form['Brand_Nm']

            if btn == 'Insert':
                cursor.execute("INSERT INTO brand VALUES (%s, %s)", (Brand_Id, Brand_Nm))
                conn.commit()
                Brand_Id, Brand_Nm = clear_textbox()
                Brand_Id = GetNewID()
                is_record = False
            elif btn == 'Update':
                cursor.execute("UPDATE brand SET Brand_Nm=%s WHERE Brand_Id=%s", (Brand_Nm, Brand_Id))
                conn.commit()
                Brand_Id, Brand_Nm = clear_textbox()
                Brand_Id = GetNewID()
                is_record = False
            elif btn == 'Delete':
                cursor.execute("DELETE FROM brand WHERE Brand_Id=%s", (Brand_Id,))
                conn.commit()
                Brand_Id, Brand_Nm = clear_textbox()
                Brand_Id = GetNewID()
                is_record = False
        except Exception as e:
            print (e)

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
    
    <script>
    
                    function formValidator() {            
                        var Brand_Id = document.getElementById("txtBrand_Id");
                        var Brand_Nm = document.getElementById("txtBrand_Nm");
                          
                                    
                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Brand_Nm, "Name Must be given") && isAlphabet(Brand_Nm, "Please enter only letters for your name")) {
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
<h1>Brand Information</h1>
<form method="POST" action="/brand">
    <p>Enter Brand ID:</p>
    <input type="text" class="form-control w-25" name="Brand_Id" value="{{ Brand_Id }}"/>
    <p>Enter Brand Name:</p>
    <input type="text" name="Brand_Nm" id="txtBrand_Nm" value="{{ Brand_Nm }}" class="form-control w-25"/><br><br>
    
    <input type="submit" value="Insert" {% if is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-primary"/>
    <input type="submit" value="Update" {% if not is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-success"/>
    <input type="submit" value="Delete" {% if not is_record %} disabled {% endif %} name="btn" class="btn btn-danger"/><br><br>
</form>
{% if brand_list %}
<table border="2px" class="table table-hover">
     <thead class="thead-dark">
    <tr>
        <th scope="row">Brand_Id</th>
        <th scope="row">Brand_Nm</th>
        <th scope="row">Select</th>
    </tr>
    </thead>
    <tbody>
    {% for row in brand_list %}
    <tr>
        <td scope="row">{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td><a href="/brand?Brand_Id={{ row[0] }}&Brand_Nm={{ row[1] }}" class="btn btn-outline-info">select</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  brand_list=brand_list,
                                  Brand_Id=Brand_Id,
                                  Brand_Nm=Brand_Nm,
                                  is_record=is_record)
