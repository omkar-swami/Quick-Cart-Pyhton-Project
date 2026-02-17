from flask import Flask, render_template_string, Blueprint
AdminDashboard=Blueprint('AdminDashboard',__name__)

@AdminDashboard.route("/AdminDashboard",methods=['GET','POST'])
def AdminDashboard_index():
    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Admin Dashboard</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">

    <!-- Google Font -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap" rel="stylesheet">

    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
            min-height: 100vh;
            margin-top:150px;
        }

        /* Dashboard Card */
        .dashboard-card {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            animation: fadeUp 1s ease forwards;
        }

        /* Heading */
        .dashboard-title {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 30px;
        }

        /* Table */
        .table {
            border-radius: 12px;
            overflow: hidden;
        }

        .table thead {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
        }

        .table thead th {
            color: blue;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.9rem;
            letter-spacing: 1px;
        }

        .table tbody tr {
            transition: all 0.4s ease;
        }

        .table tbody tr:hover {
            background: rgba(0, 198, 255, 0.15);
            transform: scale(1.01);
            box-shadow: 0 5px 15px rgba(0, 198, 255, 0.3);
        }

        /* Links */
        .table a {
            color: #ffffff;
            font-weight: 500;
            text-decoration: none;
            position: relative;
        }

        .table a::after {
            content: '';
            position: absolute;
            width: 0;
            height: 2px;
            background: #00c6ff;
            left: 0;
            bottom: -4px;
            transition: width 0.3s ease;
        }

        .table a:hover::after {
            width: 100%;
        }

        .table a:hover {
            color: #00c6ff;
        }

        /* Animation */
        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        /* Responsive */
        @media (max-width: 768px) {
            .dashboard-title {
                font-size: 1.8rem;
            }
        }
    </style>
</head>

<body class="text-white">

{% include 'navbar.html' %}

<div class="container my-5">
    <div class="dashboard-card">
        <h1 class="dashboard-title">Admin Dashboard</h1>

        <div class="table-responsive">
            <table class="table table-dark table-hover table-bordered text-center align-middle">
                <thead>
                    <tr>
                        <th>Master</th>
                        <th>List Report</th>
                        <th>Dynamic Report</th>
                        <th>Datewise Report</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><a href="{{url_for('Brand.Brand_index')}}">Brand</a></td>
                        <td><a href="{{url_for('Brandlist.Brandlist_index')}}">Brandlist</a></td>
                        <td><a href="{{url_for('BrandwiseItemmaster.BrandwiseItemmaster_index')}}">BrandwiseItemmaster</a></td>
                        <td><a href="{{url_for('DatewiseOrderMaster.DatewiseOrderMaster_index')}}">DatewiseOrderMaster</a></td>
                    </tr>
                    <tr>
                        <td><a href="{{url_for('Company.Company_index')}}">Company</a></td>
                        <td><a href="{{url_for('Companylist.Companylist_index')}}">Companylist</a></td>
                        <td><a href="{{url_for('CompanywiseItemmaster.CompanywiseItemmaster_index')}}">CompanywiseItemmaster</a></td>
                        <td><a href="{{url_for('DatewisePayment.DatewisePayment_index')}}">DatewisePayment</a></td>
                    </tr>
                    <tr>
                        <td><a href="{{url_for('Customer.Customer_index')}}">Customer</a></td>
                        <td><a href="{{url_for('Customerlist.Customerlist_index')}}">Customerlist</a></td>
                        <td><a href="{{url_for('ItemcatwiseItemmaster.ItemcatwiseItemmaster_index')}}">ItemcatwiseItemmaster</a></td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><a href="{{url_for('Itemcategory.Itemcategory_index')}}">Itemcategory</a></td>
                        <td><a href="{{url_for('Itemcategorylist.Itemcategorylist_index')}}">Itemcategorylist</a></td>
                        <td><a href="{{url_for('CompanywiseOrderDetails.CompanywiseOrderDetails_index')}}">CompanywiseOrderDetails</a></td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><a href="{{url_for('Itemmaster.Itemmaster_index')}}">Itemmaster</a></td>
                        <td><a href="{{url_for('Itemmasterlist.Itemmasterlist_index')}}">Itemmasterlist</a></td>
                        <td><a href="{{url_for('CustomerwiseOrdermaster.CustomerwiseOrdermaster_index')}}">CustomerwiseOrdermaster</a></td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><a href="{{url_for('Orderdetails.Orderdetails_index')}}">Orderdetails</a></td>
                        <td><a href="{{url_for('Orderdetailslist.Orderdetailslist_index')}}">Orderdetailslist</a></td>
                        <td><a href="{{url_for('OrderMasterwisePayment.OrderMasterwisePayment_index')}}">OrderMasterwisePayment</a></td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><a href="{{url_for('OrderMaster.OrderMaster_index')}}">OrderMaster</a></td>
                        <td><a href="{{url_for('OrderMasterlist.OrderMasterlist_index')}}">OrderMasterlist</a></td>
                        <td><a href="{{url_for('OrderMasterwiseOrderdetails.OrderMasterwiseOrderdetails_index')}}">OrderMasterwiseOrderdetails</a></td>
                        <td>-</td>
                    </tr>
                    <tr>
                        <td><a href="{{url_for('Payment.Payment_index')}}">Payment</a></td>
                        <td><a href="{{url_for('Paymentlist.Paymentlist_index')}}">Paymentlist</a></td>
                        <td><a href="{{url_for('ItemMasterwiseOrderdetails.ItemMasterwiseOrderdetails_index')}}">ItemMasterwiseOrderdetails</a></td>
                        <td>-</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

</body>
</html>


    """
    return render_template_string(html_template)