from flask import Flask, render_template_string, Blueprint, request, redirect, url_for,session
import pymysql
CustOrderRp = Blueprint('CustOrderRp', __name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

@CustOrderRp.route("/CustOrderRp", methods=['GET', 'POST'])
def CustLogin_index():
    Cust_Id=0
    OrdermasterData=[]
    OrderdetailsData=[]
    if 'Cust_id' in session:
        Cust_Id = session['Cust_id']
    conn=connection()
    cursor=conn.cursor()
    cursor.execute("select * from ordermaster where OrderCust_Id=%s",(Cust_Id,))
    OrdermasterData=cursor.fetchall()
    if request.method=='POST':
        Order_Id=request.form['Order_Id']
        cursor.execute("SELECT Order_DetId,itemmaster.Item_Nm,orderdetails.Item_Rate,Item_Qty,Item_Amt,company.Comp_NM,itemmaster.Item_Photo from orderdetails , itemmaster,company where orderdetails.Item_Id=itemmaster.Item_Id and orderdetails.Comp_id=company.Comp_Id and orderdetails.Order_Id=%s", (Order_Id,))
        OrderdetailsData = cursor.fetchall()


    html_string = """
        <!DOCTYPE html>
<html lang="en">
<head>
    <title>Customer Orders</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

    <style>
        body{
            background: linear-gradient(135deg,#eef2ff,#f8fafc);
            margin-top: 110px;
            font-family: 'Segoe UI', sans-serif;
        }

        /* ================= ORDERS TABLE ================= */
        .order-table {
            width: 95%;
            margin: auto;
            background: #fff;
            border-radius: 14px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
            text-align: center;
        }

        .order-table th {
            background: linear-gradient(135deg,#2563eb,#1e40af);
            color: #fff;
            padding: 15px;
            font-weight: 600;
            letter-spacing: .5px;
        }

        .order-table td {
            padding: 13px;
            vertical-align: middle;
            font-size: 15px;
        }

        .order-table tr {
            transition: all .2s ease-in-out;
        }

        .order-table tr:hover {
            background: #f1f5ff;
            transform: scale(1.01);
        }

        /* View Button */
        .btn-details {
            padding: 6px 18px;
            border-radius: 30px;
            font-size: 14px;
            box-shadow: 0 3px 10px rgba(37,99,235,.4);
        }

        /* ================= OVERLAY ================= */
        #orderContainer{
            position: fixed;
            inset: 0;
            background: rgba(0,0,0,.55);
            backdrop-filter: blur(6px);
            z-index: 998;
            animation: fadeBg .3s ease;
        }

        /* ================= ORDER DETAILS CARD ================= */
        #Order_detailsbox {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%,-50%);
            width: 92%;
            max-width: 950px;
            background: rgba(255,255,255,.95);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 25px 60px rgba(0,0,0,0.35);
            z-index: 999;
            animation: zoomIn .35s ease;
        }

        #Order_detailsbox h5{
            font-weight: 600;
        }

        #Order_detailsbox table {
            width: 100%;
            border-radius: 12px;
            overflow: hidden;
        }

        #Order_detailsbox th {
            background: linear-gradient(135deg,#16a34a,#065f46);
            color: white;
            padding: 12px;
            font-size: 14px;
        }

        #Order_detailsbox td {
            padding: 12px;
            font-size: 14px;
            vertical-align: middle;
        }

        #Order_detailsbox tr:hover{
            background: #ecfdf5;
        }

        .cart-img {
            border-radius: 10px;
            box-shadow: 0 6px 12px rgba(0,0,0,.25);
            transition: transform .2s;
        }

        .cart-img:hover{
            transform: scale(1.08);
        }

        .close-btn {
            float: right;
            border-radius: 30px;
            padding: 5px 14px;
        }

        /* ================= ANIMATIONS ================= */
        @keyframes zoomIn {
            from {opacity:0; transform: translate(-50%,-60%) scale(.9);}
            to {opacity:1; transform: translate(-50%,-50%) scale(1);}
        }

        @keyframes fadeBg {
            from {opacity:0;}
            to {opacity:1;}
        }
        
        .order-title-underline{
    text-align: center;
    font-size: 2rem;
    font-weight: 600;
    margin-bottom: 25px;
    position: relative;
}

.order-title-underline::after{
    content: '';
    width: 80px;
    height: 4px;
    background: linear-gradient(135deg,#2563eb,#1e40af);
    display: block;
    margin: 10px auto 0;
    border-radius: 5px;
}

    </style>
</head>

<body>

{% include 'navbar.html' %}
<h1 class="order-title-underline">Your Order Details</h1>

<!-- ================= ORDER MASTER ================= -->
{% if OrdermasterData %}
<table class="order-table">
    <tr>
        <th><i class="bi bi-hash"></i> Order ID</th>
        <th><i class="bi bi-calendar"></i> Date</th>
        <th>Amount</th>
        <th>GST</th>
        <th>Total</th>
        <th>Action</th>
    </tr>

    {% for order in OrdermasterData %}
    <tr>
        <td><span class="badge bg-secondary">{{ order[0] }}</span></td>
        <td>{{ order[1] }}</td>
        <td>₹ {{ order[3] }}</td>
        <td>₹ {{ order[4] }}</td>
        <td><strong>₹ {{ order[5] }}</strong></td>
        <td>
            <form action="/CustOrderRp" method="post">
                <input type="hidden" name="Order_Id" value="{{ order[0] }}">
                <button class="btn btn-primary btn-details">
                    <i class="bi bi-eye"></i> View
                </button>
            </form>
        </td>
    </tr>
    {% endfor %}
</table>
{% endif %}

<!-- ================= ORDER DETAILS ================= -->
{% if OrderdetailsData %}
<div id="orderContainer">
<div id="Order_detailsbox">

    <button class="btn btn-danger close-btn" onclick="closeDetails()">
        <i class="bi bi-x-lg"></i>
    </button>

    <h5 class="mb-3 text-success">
        <i class="bi bi-receipt-cutoff"></i> Order Details
    </h5>

    <table>
        <tr>
            <th>Image</th>
            <th>ID</th>
            <th>Item</th>
            <th>Company</th>
            <th>Rate</th>
            <th>Qty</th>
            <th>Total</th>
        </tr>

        {% for ord_det in OrderdetailsData %}
        <tr>
            <td>
                <img src="{{ url_for('static', filename='uploads/' + ord_det[6]) }}"
                     class="cart-img" height="85">
            </td>
            <td>{{ ord_det[0] }}</td>
            <td>{{ ord_det[1] }}</td>
            <td>{{ ord_det[5] }}</td>
            <td>₹ {{ ord_det[2] }}</td>
            <td>{{ ord_det[3] }}</td>
            <td><strong>₹ {{ ord_det[4] }}</strong></td>
        </tr>
        {% endfor %}
    </table>
</div>
</div>
{% endif %}

<script>
function closeDetails(){
    document.getElementById("orderContainer").style.display = "none";
}
</script>

</body>
</html>


        """
    return render_template_string(html_string,OrdermasterData=OrdermasterData,OrderdetailsData=OrderdetailsData)


