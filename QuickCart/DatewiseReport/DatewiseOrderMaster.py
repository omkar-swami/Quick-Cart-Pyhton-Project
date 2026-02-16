from flask import Flask, render_template_string, request, Blueprint, session
import pymysql

DatewiseOrderMaster = Blueprint('DatewiseOrderMaster',__name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@DatewiseOrderMaster.route('/datewiseOrderMaster', methods=['GET', 'POST'])
def DatewiseOrderMaster_index():
    orderlist = []
    role=""
    Total_Amount=0;
    if 'role' in session:
        role=session['role']
    if request.method == 'POST':
        fromdate = request.form.get('b1')
        todate = request.form.get('b2')
        conn = connection()
        cursor = conn.cursor()
        if role=="Admin":
            cursor.execute("SELECT Order_Id,customer.Cust_Nm,Order_Date,Order_Amt,Order_GSTAmt,Order_GrandTot FROM ordermaster,customer WHERE ordermaster.OrderCust_Id=customer.Cust_Id and Order_date BETWEEN %s AND %s",
                               (fromdate,todate))
            orderlist = cursor.fetchall()
        elif role=="ShopOwner":
            Comp_Id=session.get('Comp_id')
            cursor.execute(
                "SELECT ordermaster.Order_Id,customer.Cust_Nm,Order_Date,Order_Amt,Order_GSTAmt,Order_GrandTot,company.Comp_NM FROM ordermaster,customer,orderdetails,company WHERE ordermaster.OrderCust_Id=customer.Cust_Id and orderdetails.Comp_id=company.Comp_Id and orderdetails.Comp_id=%s and Order_date BETWEEN %s AND %s",
                (Comp_Id,fromdate, todate))
            orderlist = cursor.fetchall()
        for order in orderlist:
            Total_Amount = Total_Amount + order[5]

        cursor.close()
        conn.close()

    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Date Wise Order Report</title>

<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
<script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">

<style>
body{
    background:#f3f4f6;
    font-family:'Inter', sans-serif;
    color:#111827;
    margin-top:100px;
}

.page-wrapper{
    max-width:1200px;
    margin:auto;
    padding:40px 20px;
}

/* HEADER */
.page-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:25px;
}

.page-header h2{
    font-size:22px;
    font-weight:600;
}

/* FILTER CARD */
.filter-card{
    background:#ffffff;
    padding:20px;
    border-radius:10px;
    border:1px solid #e5e7eb;
    margin-bottom:25px;
}

.filter-card label{
    font-size:14px;
    font-weight:500;
    color:#374151;
}

.filter-card .btn{
    margin-top:28px;
}

/* TABLE CARD */
.table-card{
    background:#ffffff;
    border-radius:10px;
    border:1px solid #e5e7eb;
    overflow:hidden;
}

/* TABLE */
.table thead{
    background:#f9fafb;
}

.table th{
    font-size:13px;
    font-weight:600;
    color:#374151;
    text-transform:uppercase;
}

.table td{
    font-size:14px;
    vertical-align:middle;
}

/* TOTAL */
.total-card{
    margin-top:20px;
    background:#ecfdf5;
    border:1px solid #a7f3d0;
    padding:15px 20px;
    border-radius:8px;
    font-weight:600;
    color:#065f46;
    text-align:center;
}
</style>
</head>

<body>

{% include 'navbar.html' %}

<div class="page-wrapper">

    <!-- HEADER -->
    <div class="page-header">
        <h2>Date Wise Order Report</h2>
    </div>

    <!-- FILTER -->
    <form method="POST" action="/datewiseOrderMaster">
        <div class="filter-card">
            <div class="row g-3 align-items-end">
                <div class="col-md-3">
                    <label>From Date</label>
                    <input type="date" class="form-control" name="b1" required>
                </div>
                <div class="col-md-3">
                    <label>To Date</label>
                    <input type="date" class="form-control" name="b2" required>
                </div>
                <div class="col-md-2">
                    <button class="btn btn-success w-100">
                        Show Report
                    </button>
                </div>
            </div>
        </div>
    </form>

    {% if orderlist %}
    <!-- TABLE -->
    <div class="table-card">
        <div class="table-responsive">
            <table class="table table-hover mb-0">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Order Date</th>
                        <th>Amount</th>
                        <th>GST</th>
                        <th>Grand Total</th>
                        <th>Company</th>
                    </tr>
                </thead>
                <tbody>
                    {% for row in orderlist %}
                    <tr>
                        <td>{{ row[0] }}</td>
                        <td>{{ row[1] }}</td>
                        <td>{{ row[2] }}</td>
                        <td>₹ {{ row[3] }}</td>
                        <td>₹ {{ row[4] }}</td>
                        <td><b>₹ {{ row[5] }}</b></td>
                        <td>{{ row[6] }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>

    <!-- TOTAL -->
    <div class="total-card">
        Total Amount: ₹ {{ Total_Amount }}
    </div>
    {% endif %}

</div>

</body>
</html>

"""
    return render_template_string(html_template,
                                  orderlist=orderlist,Total_Amount=Total_Amount)

