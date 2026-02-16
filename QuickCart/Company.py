from flask import Flask, render_template_string, request,Blueprint
import pymysql
Company = Blueprint("Company",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid = 0
    qry = "SELECT MAX(Comp_Id) FROM company"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid = i[0]
        if maxid is None:
            maxid = "0"
        return int(maxid) + 1


def clear_textbox():
    return '', '', '', '', '', '', '', ''


@Company.route('/company', methods=['GET', 'POST'])
def Company_index():
    complist = []
    Comp_Id = ''
    Comp_Nm = ''
    Comp_Addr = ''
    Comp_Phone = ''
    Comp_Email = ''
    Comp_City = ''
    Comp_Descr = ''
    Comp_Password = ''
    Comp_Id = request.args.get('Comp_Id', '')
    Comp_Nm = request.args.get('Comp_Nm', '')
    Comp_Addr = request.args.get('Comp_Addr', '')
    Comp_Phone = request.args.get('Comp_Phone', '')
    Comp_Email = request.args.get('Comp_Email', '')
    Comp_City = request.args.get('Comp_City', '')
    Comp_Descr = request.args.get('Comp_Descr', '')
    Comp_Password = request.args.get('Comp_Password', '')
    is_record = bool(Comp_Id)

    if not is_record:
        Comp_Id = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Comp_Id = request.form['Comp_Id']
            Comp_Nm = request.form['Comp_Nm']
            Comp_Addr = request.form['Comp_Addr']
            Comp_Phone = request.form['Comp_Phone']
            Comp_Email = request.form['Comp_Email']
            Comp_City = request.form['Comp_City']
            Comp_Descr = request.form['Comp_Descr']
            Comp_Password = request.form['Comp_Password']

            if btn == 'Insert':
                cursor.execute("INSERT INTO company VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                               (Comp_Id, Comp_Nm, Comp_Addr, Comp_Phone, Comp_Email, Comp_City, Comp_Descr, Comp_Password))
                conn.commit()
                Comp_Id, Comp_Nm, Comp_Addr, Comp_Phone, Comp_Email, Comp_City, Comp_Descr, Comp_Password = clear_textbox()
                Comp_Id = GetNewID()
                is_record = False
            elif btn == 'Update':
                cursor.execute(
                    "UPDATE company SET Comp_Nm=%s, Comp_Addr=%s, Comp_Phone=%s, Comp_Email=%s, Comp_City=%s, Comp_Descr=%s, Comp_Password=%s  WHERE Comp_Id=%s",
                    (Comp_Nm, Comp_Addr, Comp_Phone, Comp_Email, Comp_City, Comp_Descr, Comp_Password,Comp_Id))
                conn.commit()
                Comp_Id, Comp_Nm, Comp_Addr, Comp_Phone, Comp_Email, Comp_City, Comp_Descr, Comp_Password  = clear_textbox()
                Comp_Id = GetNewID()
                is_record = False
            elif btn == 'Delete':
                cursor.execute("DELETE FROM company WHERE Comp_Id=%s", (Comp_Id))
                conn.commit()
                Comp_Id, Comp_Nm, Comp_Addr, Comp_Phone, Comp_Email, Comp_City, Comp_Descr, Comp_Password  = clear_textbox()
                Comp_Id = GetNewID()
                is_record = False
        except Exception as e:
            print(e)

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

    <script>
                    function formValidator() {            
                        var Comp_Nm = document.getElementById("txtComp_Nm");
                        var Comp_Addr=document.getElementById("txtComp_Addr");
                        var Comp_Phone = document.getElementById("txtComp_Phone");
                        var Comp_Email = document.getElementById("txtComp_Email");
                        var Comp_City = document.getElementById("txtComp_City");
                        var Comp_Descr = document.getElementById("txtComp_Descr");
                        var Comp_Password = document.getElementById("txtComp_Password");


                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Comp_Nm, "Name Must be given") && isAlphabet(Comp_Nm, "Please enter only letters for your name")) {
                             if (notEmpty(Comp_Addr, "Address Must be given") && isAlphanumeric(Comp_Addr, "Numbers and Letters Only for Address")) {
                                 if (notEmpty(Comp_Phone, "Mobile No Must be given") && validmobile(Comp_Phone) && isNumeric(Comp_Phone, "Please enter a valid Mobile no")) {
                                    if (notEmpty(Comp_Email, "Email Must be given") && emailValidator(Comp_Email, "Please enter a valid email address")) {
                                        if (notEmpty(Comp_City,"City Must be given")){
                                            if (notEmpty(Comp_Descr,"Description Must be given")){
                                                if (notEmpty(Comp_Password,"enter a password") && isValidPassword(Comp_Password,"Enter a valid Password")){
                                                    return true; 
                                                }       
                                            }
                                        }                                                 
                                    }
                                 }
                             }
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
<h1>Company Info</h1>
<form method="POST" action="/company">
    <p>Enter Company ID:(cann't changed)</p>
    <input type="text" class="form-control w-25" name="Comp_Id" value="{{ Comp_Id }}" readonly/>
    <p>Enter Company Name:</p>
    <input type="text" class="form-control w-25" name="Comp_Nm" id="txtComp_Nm" value="{{ Comp_Nm }}"/><br><br>
    <p>Enter Company Address:</p>
    <input type="text" name="Comp_Addr" class="form-control w-25" id="txtComp_Addr" value="{{ Comp_Addr }}"/><br><br>
    <p>Enter Company Phone:</p>
    <input type="text" class="form-control w-25" name="Comp_Phone" id="txtComp_Phone" value="{{ Comp_Phone }}"/><br><br>
    <p>Enter Company Email:</p>
    <input type="text" class="form-control w-25" name="Comp_Email" id="txtComp_Email" value="{{ Comp_Email }}"/><br><br>
    <p>Enter Company City</p>
    <input type="text" class="form-control w-25" name="Comp_City" id="txtComp_City" value="{{ Comp_City }}"/><br><br>
    <p>Enter Company Description:</p>
    <input type="text" class="form-control w-25" name="Comp_Descr" id="txtComp_Descr" value="{{ Comp_Descr }}"/><br><br>
    <p>Enter Company Password:</p>
    <input type="text" class="form-control w-25" name="Comp_Password" id="txtComp_Password" value="{{ Comp_Password }}"/><br><br>
    
    <input type="submit" value="Insert" {% if is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-primary"/>
    <input type="submit" value="Update" {% if not is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-success"/>
    <input type="submit" value="Delete" {% if not is_record %} disabled {% endif %} name="btn" class="btn btn-danger"/><br><br>
</form>
{% if complist %}
<table border="2px"  class="table table-hover">
    <thead>
    <tr>
        <th scope="row">Comp_Id</th>
        <th scope="col">Comp_Nm</th>
        <th scope="col">Comp_Addr</th>
        <th scope="col">Comp_Phone</th>
        <th scope="col">Comp_Email</th>
        <th scope="col">Comp_City</th>
        <th scope="col">Comp_Descr</th>
        <th scope="col">Comp_Password</th>
        <th scope="col">Select</th>
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
        <td><a href="/company?Comp_Id={{ row[0] }}&Comp_Nm={{ row[1] }}&Comp_Addr={{ row[2] }}&Comp_Phone={{ row[3] }}&Comp_Email={{ row[4] }}&Comp_City={{ row[5] }}&Comp_Descr={{ row[6] }}&Comp_Password={{ row[7] }}" class="btn btn-outline-info">select</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  complist=complist,
                                  Comp_Id=Comp_Id,
                                  Comp_Nm=Comp_Nm,
                                  Comp_Addr=Comp_Addr,
                                  Comp_Phone=Comp_Phone,
                                  Comp_Email=Comp_Email,
                                  Comp_City=Comp_City,
                                  Comp_Descr=Comp_Descr,
                                  Comp_Password=Comp_Password,
                                  is_record=is_record)

