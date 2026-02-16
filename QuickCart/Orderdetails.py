from flask import Flask, render_template_string, request,Blueprint
import pymysql

from companydashboard import companyDashboard_index

Orderdetails = Blueprint("Orderdetails",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid = 0
    qry = "SELECT MAX(Order_DetId) FROM orderdetails"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid = i[0]
        if maxid is None:
            maxid = "0"
        return int(maxid) + 1


def clear_textbox():
    return '', '' , '', '', '', '',''


@Orderdetails.route('/orderdetails', methods=['GET', 'POST'])
def Orderdetails_index():
    orderDetlist = []
    orderlist = []
    itemlist = []
    complist=[]
    Order_DetId = ''
    Order_Id = ''
    Item_Id = ''
    Item_Rate = ''
    Item_Qty = ''
    Item_Amt = ''
    Comp_Id=''
    Order_DetId = request.args.get('Order_DetId', '')
    Order_Id = request.args.get('Order_Id', '')
    Item_Id = request.args.get('Item_Id', '')
    Item_Rate = request.args.get('Item_Rate', '')
    Item_Qty = request.args.get('Item_Qty', '')
    Item_Amt = request.args.get('Item_Amt', '')
    Comp_Id=request.args.get('Comp_Id', '')
    is_record = bool(Order_DetId)

    if not is_record:
        Order_DetId = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Order_DetId = request.form['Order_DetId']
            Order_Id = request.form['Order_Id']
            Item_Id = request.form['Item_Id']
            Item_Rate = request.form['Item_Rate']
            Item_Qty = request.form['Item_Qty']
            Item_Amt = request.form['Item_Amt']
            Comp_Id=request.form['Comp_Id']
            if btn == 'Insert':
                cursor.execute("INSERT INTO orderdetails VALUES (%s,%s,%s,%s,%s,%s,%s)",
                               (Order_DetId, Order_Id, Item_Id, Item_Rate, Item_Qty, Item_Amt,Comp_Id))
                conn.commit()
                Order_DetId, Order_Id, Item_Id, Item_Rate, Item_Qty, Item_Amt,Comp_Id = clear_textbox()
                Order_DetId = GetNewID()
                is_record = False
            elif btn == 'Update':
                cursor.execute(
                    "UPDATE orderdetails SET Order_Id=%s,Item_Id=%s, Item_Rate=%s,Item_Qty=%s,Item_Amt=%s ,Comp_Id=%s WHERE Order_DetId=%s",
                    (Order_Id, Item_Id, Item_Rate, Item_Qty, Item_Amt,Comp_Id,Order_DetId))
                conn.commit()
                Order_DetId, Order_Id, Item_Id, Item_Rate, Item_Qty, Item_Amt,Comp_Id = clear_textbox()
                Order_DetId = GetNewID()
                is_record = False
            elif btn == 'Delete':
                cursor.execute("DELETE FROM orderdetails WHERE Order_DetId=%s", (Order_DetId,))
                conn.commit()
                Order_DetId, Order_Id, Item_Id, Item_Rate, Item_Qty, Item_Amt,Comp_Id = clear_textbox()
                Order_DetId = GetNewID()
                is_record = False
        except Exception as e:
            print(e)

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orderdetails")
    orderDetlist = cursor.fetchall()
    cursor.execute("SELECT * FROM ordermaster")
    orderlist = cursor.fetchall()
    cursor.execute("SELECT * FROM itemmaster")
    itemlist = cursor.fetchall()
    cursor.execute("SELECT * FROM company")
    complist = cursor.fetchall()
    cursor.close()
    conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>OrderDetails</title>

    <script>
                    function formValidator() {            
                        var Order_Id = document.getElementById("txtOrder_Id");
                        var Item_Id= document.getElementById("txtItem_Id");
                        var Item_Rate = document.getElementById("txtItem_Rate");
                        var Item_Qty = document.getElementById("txtItem_Qty");
                        var Item_Amt = document.getElementById("txtItem_Amt");
                        
                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Order_Id, "Order Id Must be given") && isNumeric(Order_Id, "Only Numbers for Order Id")) {
                            if (notEmpty(Item_Id, "Item Id Must be given") && isNumeric(Item_Id, "Only Numbers for Item Id Id")) {
                                if (notEmpty(Item_Rate, "Item Rate Must be given") && isNumeric(Item_Rate, "Please enter a Item Rate")) {
                                    if (notEmpty(Item_Qty, "Quantity  Must be given") && isNumeric(Item_Qty, "Please enter a Item Quantity")) {
                                        if (notEmpty(Item_Amt, "Item Amount Must be given") && isNumeric(Item_Amt, "Please enter a Item Amount")) {
                                                return true; 
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
<h1>OrderDetails</h1>
<form method="POST" action="/orderdetails">
    <p>Enter Order Details ID</p>
    <input type="text" class="form-control w-25" name="Order_DetId" id="Order_DetId" value="{{ Order_DetId }}"/>
    
     <p>Select Ordermaster</p>
     {% if orderlist %}
     <select  class="form-control w-25" name="Order_Id" id="txtOrder_Id">
        {% for data in orderlist %}
        <option value="{{data[0]}}"  {% if data[0] == Order_Id|int %} selected {% endif %}>{{data[0]}}</option>
        {% endfor %}
     </select>
    {% endif %}

<p>Select Itemmaster</p>
    {% if itemlist %}
    <select  class="form-control w-25" name="Item_Id" id="txtItem_Id">
        {% for data in itemlist %}
        <option value="{{data[0]}}"  {% if data[0] == Item_Id|int %} selected {% endif %}>{{data[1]}}</option>
        {% endfor %}
    </select>
    {% endif %}

    <p>Enter Item Rate</p>
    <input type="text" class="form-control w-25" name="Item_Rate" id="txtItem_Rate" value="{{Item_Rate}}"/>
    <p>Enter Item Quantity</p>
    <input type="text" class="form-control w-25" name="Item_Qty" id="txtItem_Qty" value="{{Item_Qty}}"/>
    <p>Enter Item Amount</p>
    <input type="text" class="form-control w-25" name="Item_Amt" id="txtItem_Amt" value="{{Item_Amt}}"/>
    <p>Select Company</p>
    {% if complist %}
    <select  class="form-control w-25" name="Comp_Id" id="Comp_Id" value={{Comp_Id}}>
        {% for data in complist %}
        <option value="{{data[0]}}"   {% if data[0] == Comp_Id|int %} selected {% endif %}>{{data[1]}}</option>
        {% endfor %}
    </select>
    {% endif %}
    <br><br>
    <input type="submit" value="Insert" {% if is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-primary"/>
    <input type="submit" value="Update" {% if not is_record %} disabled {% endif %} name="btn" onclick="return formValidator()" class="btn btn-success"/>
    <input type="submit" value="Delete" {% if not is_record %} disabled {% endif %} name="btn" class="btn btn-danger"/><br><br>
</form>
{% if orderDetlist %}
<table border="2px" class="table table-hover">
    <thead>
    <tr>
        <th scope="row">Order_DetId</th>
        <th scope="row">Order_Id</th>
        <th scope="row">Item_Id</th>
        <th scope="row">Item_Rate</th>
        <th scope="row">Item_Qty</th>
        <th scope="row">Item_Amt</th>
        <th scope="row">Comp_id</th>
        <th scope="row">Select</th>
    </tr>
    </thead>
    <tbody>
    {% for row in orderDetlist %}
    <tr>
        <td>{{ row[0] }}</td>
        <td>{{ row[1] }}</td>
        <td>{{ row[2] }}</td>
        <td>{{ row[3] }}</td>
        <td>{{ row[4] }}</td>
        <td>{{ row[5] }}</td>
        <td>{{ row[6] }}</td>
        <td><a href="/orderdetails?Order_DetId={{ row[0] }}&Order_Id={{ row[1] }}&Item_Id={{row[2]}}&Item_Rate={{row[3]}}&Item_Qty={{row[4]}}&Item_Amt={{row[5]}}&Comp_Id={{row[6]}}" class="btn btn-outline-info">select</a></td>
    </tr>
    {% endfor %}
    </tbody>
</table>
{% endif %}
</body>
</html>
"""
    return render_template_string(html_template,
                                  orderDetlist=orderDetlist,
                                  orderlist=orderlist,
                                  itemlist=itemlist,
                                  Order_DetId=Order_DetId,
                                  Order_Id=Order_Id,
                                  Item_Id=Item_Id,
                                  Item_Rate=Item_Rate,
                                  Item_Qty=Item_Qty,
                                  Item_Amt=Item_Amt,
                                  is_record=is_record,
                                  Comp_Id=Comp_Id,
                                  complist=complist)


