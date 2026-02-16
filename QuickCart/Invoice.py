from flask import Blueprint, session, render_template_string, request, redirect, url_for
import pymysql
Invoice = Blueprint('Invoice', __name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

@Invoice.route("/Invoice", methods=["GET", "POST"])
def Invoice_index():
    payment_id=request.args.get("payment_id")
    Order_Id=request.args.get("Order_Id")
    Cust_id=request.args.get("Cust_id")
    payment_date=request.args.get("payment_date")
    cutomerData=[]
    paymentData=[]
    OrderMaster=[]
    Orderdetails=[]
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Order_Id, Order_Date, customer.Cust_Nm,Order_Amt, Order_GSTAmt, Order_GrandTot FROM ordermaster,customer WHERE  ordermaster.OrderCust_Id=customer.Cust_Id and ordermaster.Order_Id=%s", (Order_Id,))
    OrderMaster=cursor.fetchall()
    cursor.execute("SELECT Order_DetId, Order_Id, itemmaster.Item_Nm, orderdetails.Item_Rate, Item_Qty,Item_Amt,company.Comp_NM FROM orderdetails,itemmaster,company WHERE orderdetails.Item_Id=itemmaster.Item_Id and orderdetails.Comp_id=company.Comp_Id and  Order_Id=%s", (Order_Id,))
    Orderdetails=cursor.fetchall()
    cursor.execute("SELECT * FROM payment where Order_Id=%s", (Order_Id,))
    paymentData=cursor.fetchall()
    cursor.execute("SELECT * FROM customer where Cust_Id=%s", (Cust_id,))
    cutomerData = cursor.fetchall()

    html_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Invoice</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">

    <style>
        body {
            background: #eef2f7;
            font-family: "Segoe UI", system-ui, sans-serif;
            color: #1f2937;
        }

        .invoice-wrapper {
            max-width: 760px;
            margin: 50px auto;
            background: #fff;
            box-shadow: 0 25px 50px rgba(0,0,0,.12);
            border-radius: 12px;
            overflow: hidden;
        }

        /* HEADER */
        .invoice-header {
            background: linear-gradient(135deg,#0f172a 60%,#f59e0b 60%);
            color: #fff;
            padding: 35px;
        }

        .brand {
            font-size: 28px;
            font-weight: 700;
            letter-spacing: .5px;
        }

        .brand small {
            display: block;
            font-size: 13px;
            color: #fde68a;
        }

        .invoice-title {
            font-size: 34px;
            font-weight: 800;
            text-align: right;
            letter-spacing: 2px;
        }

        /* BODY */
        .invoice-body {
            padding: 40px;
        }

        .info-title {
            font-size: 13px;
            font-weight: 700;
            margin-bottom: 8px;
            color: #f59e0b;
            text-transform: uppercase;
            letter-spacing: .8px;
        }

        .info-box p {
            margin: 4px 0;
            font-size: 14px;
        }

        /* TABLE */
        .table-responsive {
            margin-top: 30px;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 5px 15px rgba(0,0,0,.08);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }

        table thead th {
            background: #1f2937;
            color: #fff;
            font-weight: 600;
            padding: 14px;
            text-align: center;
        }

        table tbody td {
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #e5e7eb;
        }

        table tbody tr:hover {
            background: #fff7ed;
        }

        table td:nth-child(2) {
            text-align: left;
            font-weight: 600;
        }

        /* TOTALS */
        .totals {
            margin-top: 30px;
            display: flex;
            justify-content: flex-end;
        }

        .totals-box {
            width: 340px;
            background: #f9fafb;
            padding: 20px;
            border-left: 6px solid #f59e0b;
            border-radius: 8px;
        }

        .totals-box p {
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
            font-size: 14px;
        }

        .grand-total {
            margin-top: 12px;
            padding-top: 12px;
            border-top: 2px solid #f59e0b;
            font-size: 18px;
            font-weight: 800;
            display: flex;
            justify-content: space-between;
        }

        /* DELIVERY INFO */
        .delivery-box {
            margin-top: 35px;
            padding: 18px;
            background: linear-gradient(135deg,#ecfeff,#e0f2fe);
            border-left: 6px solid #0284c7;
            border-radius: 8px;
            font-size: 15px;
            font-weight: 600;
            color: #0369a1;
        }

        /* FOOTER */
        .invoice-footer {
            padding: 30px 40px;
            border-top: 1px dashed #d1d5db;
            font-size: 13px;
            color: #4b5563;
        }

        .signature {
            text-align: right;
            margin-top: 30px;
            font-weight: 700;
        }

        .btn-back {
            text-align: center;
            margin: 25px 0 35px;
        }

        @media print {
            body { background: #fff; }
            .btn-back { display: none; }
        }
    </style>
</head>

<body>

<div class="invoice-wrapper">

    <!-- HEADER -->
    <div class="invoice-header row align-items-center">
        <div class="col-md-6">
            <div class="brand">
                Quick Cart
                <small>Online Shopping Portal</small>
            </div>
        </div>
        <div class="col-md-6">
            <div class="invoice-title">INVOICE</div>
        </div>
    </div>

    <!-- BODY -->
    <div class="invoice-body">

        <!-- INFO -->
        <div class="row mb-4">
            <div class="col-md-6 info-box">
                <div class="info-title">Invoice To</div>
                {% for row in cutomerData %}
                    <p><strong>{{ row[1] }}</strong></p>
                    <p>{{ row[2] }} {{ row[5] }}</p>
                    <p>Phone: {{ row[3] }}</p>
                {% endfor %}
            </div>

            <div class="col-md-6 info-box text-end">
                <div class="info-title">Invoice Details</div>
                <p><strong>Invoice No:</strong> {{ payment_id }}</p>
                <p><strong>Order ID:</strong> {{ Order_Id }}</p>
                <p><strong>Payment Date:</strong> <span id="payDate">{{ payment_date }}</span></p>
            </div>
        </div>

        <!-- TABLE -->
        <div class="table-responsive">
            <table>
                <thead>
                    <tr>
                        <th>Sr</th>
                        <th>Item</th>
                        <th>Company</th>
                        <th>Price ₹</th>
                        <th>Qty</th>
                        <th>Total ₹</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in Orderdetails %}
                    <tr>
                        <td>{{ loop.index }}</td>
                        <td>{{ row[2] }}</td>
                        <td>{{ row[6] }}</td>
                        <td>{{ row[3] }}</td>
                        <td>{{ row[4] }}</td>
                        <td>{{ row[3] * row[4] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>

        <!-- TOTALS -->
        <div class="totals">
            <div class="totals-box">
                <p><span>Sub Total</span><span>₹ {{ OrderMaster[0][3] }}</span></p>
                <p><span>GST</span><span>₹ {{ OrderMaster[0][4] }}</span></p>
                <div class="grand-total">
                    <span>Total</span>
                    <span>₹ {{ OrderMaster[0][5] }}</span>
                </div>
            </div>
        </div>

        <!-- DELIVERY INFO -->
        <div class="delivery-box">
             Estimated Delivery Date: <span id="deliveryDate"></span>
        </div>

    </div>

    <!-- FOOTER -->
    <div class="invoice-footer">
        <p><strong>Terms & Conditions</strong></p>
        <p>
            This invoice is system generated and valid without signature.
            Goods once sold will not be returned or exchanged.
        </p>

    </div>

    <div class="btn-back">
        <a href="{{ url_for('custdashboard.custdashboard_index') }}" class="btn btn-dark px-4">
            Return to Dashboard
        </a>
    </div>

</div>

<script>
    // Calculate delivery date = payment date + 7 days
    const payDateText = document.getElementById("payDate").innerText;
    const payDate = new Date(payDateText);
    payDate.setDate(payDate.getDate() + 7);

    document.getElementById("deliveryDate").innerText =
        payDate.toDateString();
</script>

</body>
</html>



    """
    return render_template_string(html_string,OrderMaster=OrderMaster,cutomerData=cutomerData ,Orderdetails=Orderdetails, paymentData=paymentData,payment_id=payment_id ,payment_date=payment_date,Order_Id=Order_Id,table_sr=1)
