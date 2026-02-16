from flask import Flask, render_template_string, request,Blueprint
import pymysql
Payment = Blueprint("Payment",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid = 0
    qry = "SELECT MAX(Pay_Id) FROM payment"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid = i[0]
        if maxid is None:
            maxid = "0"
        return int(maxid) + 1


def clear_textbox():
    return '', '','',''


@Payment.route('/payment', methods=['GET', 'POST'])
def Payment_index():
    paylist = []
    orderlist = []
    Pay_Id = ''
    Pay_Date = ''
    Order_Id = ''
    Order_GrandTot = ''
    Pay_Id = request.args.get('Pay_Id', '')
    Pay_Date = request.args.get('Pay_Date', '')
    Order_Id = request.args.get('Order_Id', '')
    Order_GrandTot = request.args.get('Order_GrandTot', '')
    is_record = bool(Pay_Id)

    if not is_record:
        Pay_Id = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Pay_Id = request.form['Pay_Id']
            Pay_Date = request.form['Pay_Date']
            Order_Id = request.form['Order_Id']
            Order_GrandTot = request.form['Order_GrandTot']
            if btn == 'Insert':
                cursor.execute("INSERT INTO payment VALUES (%s, %s ,%s, %s)",
                               (Pay_Id, Pay_Date, Order_Id, Order_GrandTot))
                conn.commit()
                Pay_Id, Pay_Date, Order_Id, Order_GrandTot = clear_textbox()
                Pay_Id = GetNewID()
                is_record = False
            elif btn == 'Update':
                cursor.execute("UPDATE payment SET Pay_Date=%s, Order_Id=%s, Order_GrandTot=%s WHERE Pay_Id=%s",
                               (Pay_Date, Order_Id, Order_GrandTot, Pay_Id))
                conn.commit()
                Pay_Id, Pay_Date, Order_Id, Order_GrandTot = clear_textbox()
                Pay_Id = GetNewID()
                is_record = False
            elif btn == 'Delete':
                cursor.execute("DELETE FROM payment WHERE Pay_Id=%s", (Pay_Id))
                conn.commit()
                Pay_Id, Pay_Date, Order_Id, Order_GrandTot = clear_textbox()
                Pay_Id = GetNewID()
                is_record = False
        except Exception as e:
            print(e)

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM payment")
    paylist = cursor.fetchall()
    cursor.execute("SELECT * FROM ordermaster")
    orderlist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>payment</title>


<script>
                    function formValidator() {            
                        var Pay_Date = document.getElementById("txtPay_Date");
                        var Order_Id = document.getElementById("txtOrder_Id");
                        var Order_GrandTot = document.getElementById("txtOrder_GrandTot");

                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Pay_Date, "Date Must be given")) {
                            if (notEmpty(Order_Id, "Order Id Must be given") && isNumeric(Order_Id, "Only Numbers for Order Id")) {
                                if (notEmpty(Order_GrandTot, "Order GrandTotal Must be given") && isNumeric(Order_GrandTot, "Please enter a Order GrandTotal")) {
                                    return true;                                          
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
<h1>Payment Information</h1>
<form method="POST" action="/payment">
    <p>Enter Payment ID:</p>
   <input type="text" class="form-control w-25" name="Pay_Id" value="{{ Pay_Id }}"/>
    <p>Enter Payment Date:</p>
    <input type="date" class="form-control w-25" name="Pay_Date" id="txtPay_Date" value="{{Pay_Date }}"/>
    
    <p>Select Order id</p>
    {% if orderlist %}
    <select  class="form-control w-25" name="Order_Id" id="txtOrder_Id">
    <option value="0"> select the ID</option>
        {% for data in orderlist %}
        <option value="{{data[0]}}">{{data[0]}}</option>
        {% endfor %}
    </select>
    {% endif %}
    
    <p>Enter order GrandTot:</p>
    <input type="text" class="form-control w-25" name="Order_GrandTot" id="txtOrder_GrandTot" value="{{Order_GrandTot}}"/><br><br>
    
    <input type="submit" value="Insert" {% if is_record %} disabled {% endif %} name="btn" onclick="return formValidator()"  class="btn btn-primary"/>
    <input type="submit" value="Update" {% if not is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-success"/>
    <input type="submit" value="Delete" {% if not is_record %} disabled {% endif %} name="btn" class="btn btn-danger"/><br><br>
</form>
{% if paylist %}
<table border="2px" class="table table-hover">
    <thead class="thead-dark">
    <tr>
        <th scope="row">Pay_Id</th>
        <th scope="row">Pay_Date</th>
        <th scope="row">Order_Id</th>
        <th scope="row">Order_GrandTot</th>
        <th scope="row">Select</th>
    </tr>
    </thead>
    <tbody>
    {% for row in paylist %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>

        <td><a href="/payment?Pay_Id={{ row[0] }}&Pay_Date={{ row[1] }}&Order_Id={{row[2]}}&Order_GrandTot={{row[3]}}" class="btn btn-outline-info">select</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  paylist=paylist,
                                  orderlist=orderlist,
                                  Pay_Id=Pay_Id,
                                  Pay_Date=Pay_Date,
                                  Order_Id=Order_Id,
                                  Order_GrandTot=Order_GrandTot,
                                  is_record=is_record)

