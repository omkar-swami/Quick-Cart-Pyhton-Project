from flask import Flask, render_template_string, request,Blueprint
import pymysql
Customer = Blueprint("Customer",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid=0
    qry="SELECT MAX(Cust_Id) FROM customer"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid=i[0]
        if maxid is None:
            maxid="0"
        return int(maxid) + 1

def clear_textbox():
    return '', '', '', '', '', '', ''

@Customer.route('/customer', methods=['GET', 'POST'])
def Customer_index():
    custlist = []
    Cust_Id = ''
    Cust_Nm = ''
    Cust_Addr = ''
    Cust_Phone = ''
    Cust_Email = ''
    Cust_Pincode = ''
    Cust_Password = ''
    Cust_Id = request.args.get('Cust_Id', '')
    Cust_Nm = request.args.get('Cust_Nm', '')
    Cust_Addr = request.args.get('Cust_Addr', '')
    Cust_Phone = request.args.get('Cust_Phone', '')
    Cust_Email = request.args.get('Cust_Email', '')
    Cust_Pincode = request.args.get('Cust_Pincode', '')
    Cust_Password = request.args.get('Cust_Password', '')
    is_record = bool(Cust_Id)

    if not is_record:
        Cust_Id = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Cust_Id =  request.form['Cust_Id']
            Cust_Nm = request.form['Cust_Nm']
            Cust_Addr =  request.form['Cust_Addr']
            Cust_Phone =  request.form['Cust_Phone']
            Cust_Email =  request.form['Cust_Email']
            Cust_Pincode =  request.form['Cust_Pincode']
            Cust_Password =  request.form['Cust_Password']

            if btn == 'Insert':
                cursor.execute("INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s,%s)", (Cust_Id, Cust_Nm,Cust_Addr,Cust_Phone,Cust_Email,Cust_Pincode,Cust_Password))
                conn.commit()
                Cust_Id, Cust_Nm,Cust_Addr,Cust_Phone,Cust_Email,Cust_Pincode,Cust_Password= clear_textbox()
                Cust_Id = GetNewID()
                is_record = False
            elif btn == 'Update':
                cursor.execute("UPDATE customer SET Cust_Nm=%s, Cust_Addr=%s, Cust_Phone=%s, Cust_Email=%s, Cust_Pincode=%s, Cust_Password=%s  WHERE Cust_Id=%s", (Cust_Nm,Cust_Addr,Cust_Phone,Cust_Email,Cust_Pincode,Cust_Password,Cust_Id))
                conn.commit()
                Cust_Id, Cust_Nm,Cust_Addr,Cust_Phone,Cust_Email,Cust_Pincode,Cust_Password = clear_textbox()
                Cust_Id = GetNewID()
                is_record = False
            elif btn == 'Delete':
                cursor.execute("DELETE FROM customer WHERE Cust_Id=%s", (Cust_Id))
                conn.commit()
                Cust_Id, Cust_Nm, Cust_Addr, Cust_Phone, Cust_Email, Cust_Pincode, Cust_Password = clear_textbox()
                Cust_Id = GetNewID()
                is_record = False
        except Exception as e:
            print (e)

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
    
    <script>
                    function formValidator() {            
                        var Cust_Nm = document.getElementById("txtCust_Nm");
                        var Cust_Addr = document.getElementById("txtCust_Addr");
                        var Cust_Phone=document.getElementById("txtCust_Phone");
                        var Cust_Email = document.getElementById("txtCust_Email");
                        var Cust_Pincode = document.getElementById("txtCust_Pincode");
                        var Cust_Password = document.getElementById("txtCust_Password");
                          
                                    
                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Cust_Nm, "Name Must be given") && isAlphabet(Cust_Nm, "Please enter only letters for your name")) {
                             if (notEmpty(Cust_Addr, "Address Must be given") && isAlphanumeric(Cust_Addr, "Numbers and Letters Only for Address")) {
                                 if (notEmpty(Cust_Phone, "Mobile No Must be given") && validmobile(Cust_Phone) && isNumeric(Cust_Phone, "Please enter a valid Mobile no")) {
                                     if (notEmpty(Cust_Email, "Email Must be given") && emailValidator(Cust_Email, "Please enter a valid email address")) {
                                        if (notEmpty(Cust_Pincode,"Pincode Must be given")){
                                            if (notEmpty(Cust_Password,"enter a password") && isValidPassword(Cust_Password,"Enter a valid Password")){
                                                return true;    
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
<h1>Customer Info</h1>
<form method="POST" action="/customer">
    <p>Enter Customer ID:</p>
    <input type="text" class="form-control w-25" name="Cust_Id" value="{{ Cust_Id }}"/>
    <p>Enter Customer Name:</p>
    <input type="text" class="form-control w-25" name="Cust_Nm" id="txtCust_Nm" value="{{ Cust_Nm }}"/><br><br>
    <p>Enter Customer Address:</p>
    <input type="text" class="form-control w-25" name="Cust_Addr" id="txtCust_Addr" value="{{ Cust_Addr }}"/><br><br>
    <p>Enter Customer Phone:</p>
    <input type="text" class="form-control w-25" name="Cust_Phone" id="txtCust_Phone" value="{{ Cust_Phone }}"/><br><br>
    <p>Enter Customer Email:</p>
    <input type="text" class="form-control w-25" name="Cust_Email" id="txtCust_Email" value="{{ Cust_Email }}"/><br><br>
    <p>Enter Customer Pincode</p>
    <input type="text" class="form-control w-25" name="Cust_Pincode" id="txtCust_Pincode" value="{{ Cust_Pincode }}"/><br><br>
    <p>Enter Customer Password:</p>
    <input type="text" class="form-control w-25" name="Cust_Password" id="txtCust_Password" value="{{ Cust_Password }}"/><br><br>
    
    <input type="submit" value="Insert" {% if is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-primary"/>
    <input type="submit" value="Update" {% if not is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-success"/>
    <input type="submit" value="Delete" {% if not is_record %} disabled {% endif %} name="btn" class="btn btn-danger"/><br><br>
</form>
{% if custlist %}
<table border="2px" class="table table-hover">
    <thead>
    <tr>
        <th scope="row">Cust_Id</th>
        <th scope="row">Cust_Nm</th>
        <th scope="row">Cust_Addr</th>
        <th scope="row">Cust_Phone</th>
        <th scope="row">Cust_Email</th>
        <th scope="row">Cust_Pincode</th>
        <th scope="row">Cust_Password</th>
        <th scope="row">Select</th>
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
        <td><a href="/customer?Cust_Id={{ row[0] }}&Cust_Nm={{ row[1] }}&Cust_Addr={{ row[2] }}&Cust_Phone={{ row[3] }}&Cust_Email={{ row[4] }}&Cust_Pincode={{ row[5] }}&Cust_Password={{ row[6] }}" class="btn btn-outline-info">select</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  custlist=custlist,
                                  Cust_Id=Cust_Id,
                                  Cust_Nm=Cust_Nm,
                                  Cust_Addr=Cust_Addr,
                                  Cust_Phone=Cust_Phone,
                                  Cust_Email=Cust_Email,
                                  Cust_Pincode=Cust_Pincode,
                                  Cust_Password=Cust_Password,
                                  is_record=is_record)

