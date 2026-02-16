from flask import Blueprint, session, render_template_string, request, redirect, url_for
import pymysql
checkout = Blueprint('checkout', __name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')
def GetNewOrderID():
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
def GetNewOrderDetailID():
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
def GetNewPaymentID():
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


# ---------------- CHECKOUT ROUTE ----------------
@checkout.route("/checkout", methods=["GET", "POST"])
def checkout_index():

    # ---------- DEFAULT VALUES ----------
    Cust_id = 0
    Order_Id = GetNewOrderID()
    payment_id = GetNewPaymentID()

    Cust_Nm = ""
    Cust_Addr = ""
    Cust_Phone = ""

    cart = []
    No_of_items = 0
    tot_amount = 0
    Gst_amount = 0
    payment_amount = 0
    if "Cust_id" in session:
        Cust_id = session["Cust_id"]
    # ---------- GET REQUEST ----------
    if request.method == "GET":
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM customer WHERE Cust_Id=%s", (Cust_id,))
        custlist = cursor.fetchall()

        if custlist:
            Cust_Nm = custlist[0][1]
            Cust_Addr = custlist[0][2] + " " + custlist[0][5]
            Cust_Phone = custlist[0][3]

        if "cart" in session:
            cart = session["cart"]
            No_of_items = len(cart)

        for item in cart:
            item_total = item["Item_Qty"] * item["Item_Rate"]
            tot_amount += item_total

        Gst_amount = (tot_amount * 5) / 100
        payment_amount = tot_amount + Gst_amount

    # ---------- POST REQUEST ----------
    if request.method == "POST":
        Order_Id=request.form["Order_Id"]
        Order_Date=request.form["order_date"]
        OrderCust_Id=session["Cust_id"]
        Order_Amt=request.form["tot_amount"]
        Order_GSTAmt=request.form["Gst_amount"]
        Order_GrandTot=request.form["payment_amount"]
        conn = connection()
        cursor = conn.cursor()
        # add to ordermaster
        cursor.execute("INSERT INTO ordermaster VALUES (%s,%s,%s,%s,%s,%s)",
                       (Order_Id, Order_Date, OrderCust_Id, Order_Amt, Order_GSTAmt, Order_GrandTot))
        conn.commit()

        # add to order details
        cart=[]
        if 'cart' in session:
            cart=session["cart"]
        for item in cart:
            Order_DetId=GetNewOrderDetailID()
            Item_Id=item["Item_id"]
            Item_Rate=item["Item_Rate"]
            Item_Qty=item["Item_Qty"]
            Item_Amt=item["Item_Rate"]*item["Item_Qty"]
            Comp_Id=item["Comp_Id"]
            cursor.execute("INSERT INTO orderdetails VALUES (%s,%s,%s,%s,%s,%s,%s)",
                           (Order_DetId, Order_Id, Item_Id, Item_Rate, Item_Qty, Item_Amt,Comp_Id))
            conn.commit()
            cursor.execute("UPDATE itemmaster SET Item_Stock=Item_Stock-%s  WHERE Item_Id=%s",(Item_Qty,Item_Id))
            conn.commit()

         #Add the data to the payment
        cursor.execute("INSERT INTO payment VALUES (%s, %s ,%s, %s)",
                       (payment_id, Order_Date, Order_Id, Order_GrandTot))
        conn.commit()
        session.pop("cart", None)
        return redirect(url_for("Invoice.Invoice_index",payment_id=payment_id,
            payment_date=Order_Date,
            Order_Id=Order_Id,
            Cust_id=OrderCust_Id
        ))

    # ---------- HTML TEMPLATE ----------
    html_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Checkout</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

    <style>
        body{
            background: linear-gradient(135deg,#eef2ff,#f8fafc);
            margin-top:120px;
            font-family: "Segoe UI", system-ui, sans-serif;
        }

        .wrapper{
            max-width: 900px;
            margin: auto;
        }

        /* Glass Card */
        .card-box{
            background: rgba(255,255,255,.95);
            backdrop-filter: blur(10px);
            padding: 30px;
            border-radius: 18px;
            box-shadow: 0 25px 50px rgba(0,0,0,.12);
            animation: fadeUp .4s ease;
        }

        /* Page Title */
        .title{
            text-align: center;
            font-size: 26px;
            font-weight: 700;
            margin-bottom: 30px;
            background: linear-gradient(135deg,#2563eb,#1e40af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            letter-spacing: .5px;
        }

        /* Section Headers */
        .section{
            font-weight: 600;
            margin: 30px 0 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid #e5e7eb;
            color: #1f2937;
        }

        /* Inputs */
        .form-control,
        .form-select{
            height: 42px;
            border-radius: 10px;
            border: 1px solid #d1d5db;
            font-size: 14px;
        }

        .form-control:focus,
        .form-select:focus{
            border-color: #2563eb;
            box-shadow: 0 0 0 .2rem rgba(37,99,235,.15);
        }

        label{
            font-size: 13px;
            font-weight: 600;
            color: #374151;
        }

        /* Final Amount Highlight */
        .final{
            background: linear-gradient(135deg,#ecfeff,#e0f2fe);
            font-weight: 700;
            color: #0369a1;
        }

        /* Pay Button */
        .btn-pay{
            background: linear-gradient(135deg,#2563eb,#1e40af);
            color: white;
            padding: 10px 45px;
            border: none;
            border-radius: 30px;
            font-size: 16px;
            font-weight: 600;
            box-shadow: 0 10px 25px rgba(37,99,235,.45);
            transition: all .25s ease;
        }

        .btn-pay:hover{
            transform: translateY(-2px);
            box-shadow: 0 15px 35px rgba(37,99,235,.6);
        }

        /* Animations */
        @keyframes fadeUp{
            from{
                opacity:0;
                transform: translateY(20px);
            }
            to{
                opacity:1;
                transform: translateY(0);
            }
        }
    </style>
</head>

<body>

{% include 'navbar.html' %}

<div class="wrapper">
<div class="card-box">

<div class="title">
    Make a Payment
</div>

<form method="POST">

<!-- ================= ORDER INFO ================= -->
<div class="section">Order Information</div>

<div class="row g-3">
    <div class="col-md-4">
        <label>Payment ID</label>
        <input class="form-control" value="{{ payment_id }}" readonly>
    </div>

    <div class="col-md-4">
        <label>Order Date</label>
        <input type="date" class="form-control" id="order_date" name="order_date" readonly>
    </div>

    <div class="col-md-4">
        <label>Order ID</label>
        <input class="form-control" name="Order_Id" value="{{ Order_Id }}" readonly>
    </div>
</div>

<div class="row g-3 mt-1">
    <div class="col-md-6">
        <label>Customer Name</label>
        <input class="form-control" value="{{ Cust_Nm }}" readonly>
    </div>
    <div class="col-md-6">
        <label>Phone</label>
        <input class="form-control" value="{{ Cust_Phone }}" readonly>
    </div>
</div>

<div class="mt-3">
    <label>Delivery Address</label>
    <input class="form-control" value="{{ Cust_Addr }}" readonly>
</div>

<!-- ================= PAYMENT SUMMARY ================= -->
<div class="section">Payment Summary</div>

<div class="row g-3">
    <div class="col-md-3">
        <label>Items</label>
        <input class="form-control" value="{{ No_of_items }}" readonly>
    </div>
    <div class="col-md-3">
        <label>Total Amount</label>
        <input class="form-control" name="tot_amount" value="{{ tot_amount }}" readonly>
    </div>
    <div class="col-md-3">
        <label>GST (5%)</label>
        <input class="form-control" name="Gst_amount" value="{{ Gst_amount }}" readonly>
    </div>
    <div class="col-md-3">
        <label>Final Payable</label>
        <input class="form-control final" name="payment_amount" value="{{ payment_amount }}" readonly>
    </div>
</div>

<!-- ================= PAYMENT METHOD ================= -->
<div class="section">Payment Method</div>

<div class="row g-3">
    <div class="col-md-4">
        <label>Payment Type</label>
        <select class="form-select" name="payment_type" onchange="togglePay()" required>
            <option value="">Select</option>
            <option>Cash</option>
            <option>UPI</option>
            <option>Credit_Card</option>
        </select>
    </div>

    <div class="col-md-4" id="upi" style="display:none">
        <label>UPI ID</label>
        <input class="form-control" name="upi_id" placeholder="example@upi">
    </div>

    <div class="col-md-4" id="card" style="display:none">
        <label>Card Number</label>
        <input class="form-control" name="card_number" maxlength="16" placeholder="XXXX XXXX XXXX XXXX">
    </div>
</div>

<div class="text-center mt-5">
    <button class="btn-pay">
        <i class="bi bi-lock-fill"></i> Confirm Payment
    </button>
</div>

</form>
</div>
</div>

<script>
document.getElementById("order_date").value =
    new Date().toISOString().split('T')[0];

function togglePay(){
    let t=document.querySelector("[name=payment_type]").value;
    document.getElementById("upi").style.display=(t=="UPI")?"block":"none";
    document.getElementById("card").style.display=(t=="Credit_Card")?"block":"none";
}
</script>

</body>
</html>

"""

    return render_template_string(
        html_string,
        Cust_id=Cust_id,
        Order_Id=Order_Id,
        payment_id=payment_id,
        Cust_Nm=Cust_Nm,
        Cust_Addr=Cust_Addr,
        Cust_Phone=Cust_Phone,
        No_of_items=No_of_items,
        tot_amount=tot_amount,
        Gst_amount=Gst_amount,
        payment_amount=payment_amount,
        cart=cart
    )









