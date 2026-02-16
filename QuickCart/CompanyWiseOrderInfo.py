from flask import Flask, render_template_string, request, Blueprint, session
import pymysql

CompanyWiseOrderInfo = Blueprint('CompanyWiseOrderInfo', __name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


@CompanyWiseOrderInfo.route('/CompanyWiseOrderInfo', methods=['GET', 'POST'])
def CompanyWiseOrderInfo_index():
    orderData=[]
    Total_amt=0
    Comp_id=0
    if 'Comp_id' in session:
        Comp_id=session['Comp_id']

    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Order_DetId , itemmaster.Item_Nm,orderdetails.Item_Rate,Item_Qty,orderdetails.Item_Amt,customer.Cust_Nm,ordermaster.Order_Date FROM ordermaster,orderdetails,itemmaster,customer,company WHERE orderdetails.Order_Id=ordermaster.Order_Id and ordermaster.OrderCust_Id=customer.Cust_Id and orderdetails.Item_Id=itemmaster.Item_Id and orderdetails.Comp_id=company.Comp_Id and orderdetails.Comp_id=%s",(Comp_id,))
    orderData=cursor.fetchall()
    for data in orderData:
        Total_amt=Total_amt+data[4]

    html_template = """
   <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Company Dashboard</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

    <!-- Custom CSS -->
    <style>
        body {
            background: #f4f6f9;
            font-family: 'Poppins', sans-serif;
            margin-top: 100px;
        }

        .page-title {
            font-weight: 700;
            color: #0d6efd;
            margin-bottom: 25px;
        }

        .card {
            border: none;
            border-radius: 16px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        }

        table {
            border-radius: 14px;
            overflow: hidden;
        }

        thead {
            background: linear-gradient(90deg, #0d6efd, #0a58ca);
            color: white;
        }

        th, td {
            vertical-align: middle;
            text-align: center;
        }

        tbody tr:hover {
            background-color: #eef4ff;
            transition: 0.2s;
        }

        .total-box {
            background: linear-gradient(90deg, #198754, #20c997);
            color: white;
            border-radius: 14px;
            padding: 18px;
            font-size: 20px;
            font-weight: 600;
            text-align: center;
            margin-top: 20px;
            box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        }
    </style>
</head>

<body>

{% include 'navbar.html' %}

<div class="container">

    <h2 class="page-title text-center">Company Order Dashboard</h2>

    <!-- TABLE CARD -->
    <div class="card p-4">

        <div class="table-responsive">
            <table class="table table-hover align-middle">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Order Date</th>
                        <th>Item Name</th>
                        <th>Rate</th>
                        <th>Quantity</th>
                        <th>Amount</th>
                    </tr>
                </thead>

                <tbody>
                {% if orderData %}
                    {% for data in orderData %}
                    <tr>
                        <td>{{ data[0] }}</td>
                        <td>{{ data[5] }}</td>
                        <td>{{ data[6] }}</td>
                        <td>{{ data[1] }}</td>
                        <td>₹ {{ data[2] }}</td>
                        <td>{{ data[3] }}</td>
                        <td class="fw-bold text-success">₹ {{ data[4] }}</td>
                    </tr>
                    {% endfor %}
                {% else %}
                    <tr>
                        <td colspan="7" class="text-muted">No Orders Found</td>
                    </tr>
                {% endif %}
                </tbody>
            </table>
        </div>

    </div>

    <!-- TOTAL AMOUNT -->
    {% if orderData %}
    <div class="total-box">
        Total Sales Amount : ₹ {{ Total_amt }}
    </div>
    {% endif %}

</div>

</body>
</html>


"""
    return render_template_string(html_template,orderData=orderData,Total_amt=Total_amt)