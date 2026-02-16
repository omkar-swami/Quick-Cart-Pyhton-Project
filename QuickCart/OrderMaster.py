from flask import Flask, render_template_string, request,Blueprint
import pymysql
OrderMaster = Blueprint("OrderMaster",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid = 0
    qry = "SELECT MAX(Order_Id) FROM ordermaster"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid = i[0]
        if maxid is None:
            maxid = "0"
        return int(maxid) + 1


def clear_textbox():
    return '', '', '', '', '', ''


@OrderMaster.route('/ordermaster', methods=['GET', 'POST'])
def OrderMaster_index():
    orderlist = []
    ordercustlist=[]
    ordercomplist = []
    Order_Id = ''
    Order_Date = ''
    OrderCust_Id = ''
    OrderComp_Id = 000
    Order_Amt = ''
    Order_GSTAmt = ''
    Order_GrandTot = ''
    Order_Id = request.args.get('Order_Id', '')
    Order_Date = request.args.get('Order_Date', '')
    OrderCust_Id = request.args.get('OrderCust_Id', '')

    Order_Amt = request.args.get('Order_Amt', '')
    Order_GSTAmt = request.args.get('Order_GSTAmt', '')
    Order_GrandTot = request.args.get('Order_GrandTot', '')
    is_record = bool(Order_Id)

    if not is_record:
        Order_Id = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Order_Id = request.form['Order_Id']
            Order_Date = request.form['Order_Date']
            OrderCust_Id = request.form['OrderCust_Id']

            Order_Amt = request.form['Order_Amt']
            Order_GSTAmt = request.form['Order_GSTAmt']
            Order_GrandTot = request.form['Order_GrandTot']

            if btn == 'Insert':
                cursor.execute("INSERT INTO ordermaster VALUES (%s,%s,%s,%s,%s,%s)",
                               (Order_Id, Order_Date, OrderCust_Id, Order_Amt, Order_GSTAmt, Order_GrandTot))
                conn.commit()
                Order_Id, Order_Date, OrderCust_Id, Order_Amt, Order_GSTAmt, Order_GrandTot = clear_textbox()
                Order_Id = GetNewID()
                is_record = False
            elif btn == 'Update':
                cursor.execute(
                    "UPDATE ordermaster SET Order_Date=%s, OrderCust_Id=%s,  Order_Amt=%s, Order_GSTAmt=%s, Order_GrandTot=%s  WHERE Order_Id=%s",
                    (Order_Date, OrderCust_Id, Order_Amt, Order_GSTAmt, Order_GrandTot,Order_Id))
                conn.commit()
                Order_Id, Order_Date, OrderCust_Id, Order_Amt, Order_GSTAmt, Order_GrandTot  = clear_textbox()
                Order_Id = GetNewID()
                is_record = False
            elif btn == 'Delete':
                cursor.execute("DELETE FROM ordermaster WHERE Order_Id=%s", (Order_Id))
                conn.commit()
                Order_Id, Order_Date, OrderCust_Id, Order_Amt, Order_GSTAmt, Order_GrandTot  = clear_textbox()
                Order_Id = GetNewID()
                is_record = False
        except Exception as e:
            print(e)

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ordermaster")
    orderlist = cursor.fetchall()
    cursor.execute("SELECT * FROM customer")
    ordercustlist = cursor.fetchall()
    cursor.execute("SELECT * FROM company")
    ordercomplist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ordermaster</title>

    <script>
                    function formValidator() {            
                        var Order_Date = document.getElementById("txtOrder_Date");
                        var OrderCust_Id=document.getElementById("txtOrderCust_Id");
                        var OrderComp_Id = document.getElementById("txtOrderComp_Id");
                        var Order_Amt = document.getElementById("txtOrder_Amt");
                        var Order_GSTAmt = document.getElementById("txtOrder_GSTAmt");
                        var Order_GrandTot = document.getElementById("txtOrder_GrandTot");


                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Order_Date, "Date Must be given")) {
                            if (notEmpty(OrderCust_Id, "Order Customer Id Must be given") && isNumeric(OrderCust_Id, "Only Numbers for Order Customer Id")) {
                                if (notEmpty(OrderComp_Id, "Order Company Id Must be given") && isNumeric(OrderComp_Id, "Only Numbers for Order Company Id")) {
                                    if (notEmpty(Order_Amt, "Order Amount Must be given") && isNumeric(Order_Amt, "Please enter a Order Amount")) {
                                        if (notEmpty(Order_GSTAmt, "Order GSTAmount Must be given") && isNumeric(Order_GSTAmt, "Please enter a Order GSTAmount")) {
                                            if (notEmpty(Order_GrandTot, "Order GrandTotal Must be given") && isNumeric(Order_GrandTot, "Please enter a Order GrandTotal")) {
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
<h1>OrderMaster Info</h1>
<form method="POST" action="/ordermaster">
    <p>Enter Order ID:</p>
    <input type="text" class="form-control w-25" name="Order_Id" value="{{ Order_Id }}"/>
    <p>Enter Order Date:</p>
    <input type="date" class="form-control w-25" name="Order_Date" id="txtOrder_Date" value="{{ Order_Date }}"/><br><br>
    
    <p>Select Customer </p>
    {% if ordercustlist %}
    <select  class="form-control w-25" name="OrderCust_Id" id="txtOrderCust_Id">
        {% for data in ordercustlist %}
        <option value="{{data[0]}}">{{data[1]}}</option>
        {% endfor %}
    </select>
    {% endif %}
   
    
    <p>Enter Order Amount:</p>
    <input type="text" class="form-control w-25" name="Order_Amt" id="txtOrder_Amt" value="{{ Order_Amt }}"/><br><br>
    <p>Enter Order GSTAmount</p>
    <input type="text" class="form-control w-25" name="Order_GSTAmt" id="txtOrder_GSTAmt" value="{{ Order_GSTAmt }}"/><br><br>
    <p>Enter Order GrandTotal:</p>
    <input type="text" class="form-control w-25" name="Order_GrandTot" id="txtOrder_GrandTot" value="{{ Order_GrandTot }}"/><br><br>
    
    <input type="submit" value="Insert" {% if is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-primary"/>
    <input type="submit" value="Update" {% if not is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-success"/>
    <input type="submit" value="Delete" {% if not is_record %} disabled {% endif %} name="btn" class="btn btn-danger"/><br><br>
</form>
{% if orderlist %}
<table border="2px" class="table table-hover">
    <thead>
    <tr>
        <th scope="row">Order_Id</th>
        <th scope="row">Order_Date</th>
        <th scope="row">OrderCust_Id</th>
        
        <th scope="row">Order_Amt</th>
        <th scope="row">Order_GSTAmt</th>
        <th scope="row">Order_GrandTot</th>
        <th scope="row">Select</th>
    </tr>
    </thead>
    <tbody>
    {% for row in orderlist %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>
        <td>{{ row[4] }}</td>
        <td>{{ row[5] }}</td>
        <td><a href="/ordermaster?Order_Id={{ row[0] }}&Order_Date={{ row[1] }}&OrderCust_Id={{ row[2] }}&Order_Amt={{ row[4] }}&Order_GSTAmt={{ row[5] }}&Order_GrandTot={{ row[5] }}" class="btn btn-outline-info">select</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  orderlist=orderlist,
                                  ordercustlist=ordercustlist,
                                  ordercomplist=ordercomplist,
                                  Order_Id=Order_Id,
                                  Order_Date=Order_Date,
                                  OrderCust_Id=OrderCust_Id,

                                  Order_Amt=Order_Amt,
                                  Order_GSTAmt=Order_GSTAmt,
                                  Order_GrandTot=Order_GrandTot,
                                  is_record=is_record)

