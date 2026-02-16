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

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
</head>
<body class="bg-dark text-white">
  {% include 'navbar.html' %}
<div class="container my-5">
    <h1 class="text-center text-info mb-4">Admin Dashboard</h1>

    <div class="table-responsive">
        <table class="table table-hover table-dark table-bordered text-center align-middle">
            <thead class="table-info text-dark">
                <tr>
                    <th>Master</th>
                    <th>List Report</th>
                    <th>Dynamic Report</th>
                    <th>Datewise Report</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><a href="{{url_for('Brand.Brand_index')}}" class="text-white text-decoration-none">Brand</a></td>
                    <td><a href="{{url_for('Brandlist.Brandlist_index')}}" class="text-white text-decoration-none">Brandlist</a></td>
                    <td><a href="{{url_for('BrandwiseItemmaster.BrandwiseItemmaster_index')}}" class="text-white text-decoration-none">BrandwiseItemmaster</a></td>
                    <td><a href="{{url_for('DatewiseOrderMaster.DatewiseOrderMaster_index')}}" class="text-white text-decoration-none">DatewiseOrderMaster</a></td>
                </tr>
                <tr>
                    <td><a href="{{url_for('Company.Company_index')}}" class="text-white text-decoration-none">Company</a></td>
                    <td><a href="{{url_for('Companylist.Companylist_index')}}" class="text-white text-decoration-none">Companylist</a></td>
                    <td><a href="{{url_for('CompanywiseItemmaster.CompanywiseItemmaster_index')}}" class="text-white text-decoration-none">CompanywiseItemmaster</a></td>
                    <td><a href="{{url_for('DatewisePayment.DatewisePayment_index')}}" class="text-white text-decoration-none">DatewisePayment</a></td>
                </tr>
                <tr>
                    <td><a href="{{url_for('Customer.Customer_index')}}" class="text-white text-decoration-none">Customer</a></td>
                    <td><a href="{{url_for('Customerlist.Customerlist_index')}}" class="text-white text-decoration-none">Customerlist</a></td>
                    <td><a href="{{url_for('ItemcatwiseItemmaster.ItemcatwiseItemmaster_index')}}" class="text-white text-decoration-none">ItemcatwiseItemmaster</a></td>
                    <td>-</td>
                </tr>
                <tr>
                    <td><a href="{{url_for('Itemcategory.Itemcategory_index')}}" class="text-white text-decoration-none">Itemcategory</a></td>
                    <td><a href="{{url_for('Itemcategorylist.Itemcategorylist_index')}}" class="text-white text-decoration-none">Itemcategorylist</a></td>
                    <td><a href="{{url_for('CompanywiseOrderDetails.CompanywiseOrderDetails_index')}}" class="text-white text-decoration-none">Company Wise orderDetails</a></td>
                    <td>-</td>
                </tr>
                <tr>
                    <td><a href="{{url_for('Itemmaster.Itemmaster_index')}}" class="text-white text-decoration-none">Itemmaster</a></td>
                    <td><a href="{{url_for('Itemmasterlist.Itemmasterlist_index')}}" class="text-white text-decoration-none">Itemmasterlist</a></td>
                    <td><a href="{{url_for('CustomerwiseOrdermaster.CustomerwiseOrdermaster_index')}}" class="text-white text-decoration-none">CustomerwiseOrdermaster</a></td>
                    <td>-</td>
                </tr>
                <tr>
                    <td><a href="{{url_for('Orderdetails.Orderdetails_index')}}" class="text-white text-decoration-none">Orderdetails</a></td>
                    <td><a href="{{url_for('Orderdetailslist.Orderdetailslist_index')}}" class="text-white text-decoration-none">Orderdetailslist</a></td>
                    <td><a href="{{url_for('OrderMasterwisePayment.OrderMasterwisePayment_index')}}" class="text-white text-decoration-none">OrderMasterwisePayment</a></td>
                    <td>-</td>
                </tr>
                <tr>
                    <td><a href="{{url_for('OrderMaster.OrderMaster_index')}}" class="text-white text-decoration-none">OrderMaster</a></td>
                    <td><a href="{{url_for('OrderMasterlist.OrderMasterlist_index')}}" class="text-white text-decoration-none">OrderMasterlist</a></td>
                    <td><a href="{{url_for('OrderMasterwiseOrderdetails.OrderMasterwiseOrderdetails_index')}}" class="text-white text-decoration-none">OrderMasterwiseOrderdetails</a></td>
                    <td>-</td>
                </tr>
                <tr>
                    <td><a href="{{url_for('Payment.Payment_index')}}" class="text-white text-decoration-none">Payment</a></td>
                    <td><a href="{{url_for('Paymentlist.Paymentlist_index')}}" class="text-white text-decoration-none">Paymentlist</a></td>
                    <td><a href="{{url_for('ItemMasterwiseOrderdetails.ItemMasterwiseOrderdetails_index')}}" class="text-white text-decoration-none">ItemMasterwiseOrderdetails</a></td>
                    <td>-</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>

</body>
</html>

    """
    return render_template_string(html_template)