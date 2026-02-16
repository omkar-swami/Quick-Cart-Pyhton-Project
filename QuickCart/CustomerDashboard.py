from flask import Flask, render_template_string, Blueprint, request, redirect, url_for, session

custdashboard = Blueprint('custdashboard', __name__)

@custdashboard.route("/custdashboard", methods=['GET', 'POST'])
def custdashboard_index():
    Cust_Name=""
    if "Cust_Name" in session:
        Cust_Name=session["Cust_Name"]

    html_string = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>User Dashboard</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

    <style>
        /* General body styling */
        body {
            background: #0a1f2e; /* Dark blue background */
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            font-family: 'Poppins', sans-serif;
            color: #fff;
        }

        /* Dashboard container */
        .dashboard-container {
            background: #112a3a;
            width: 500px;
            padding: 50px 40px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(0,0,0,0.6);
            animation: containerFade 1s ease-in-out;
        }

        /* Dashboard title */
        .dashboard-container h2 {
            margin-bottom: 40px;
            font-weight: 700;
            color: #1ec6ff; /* Bright blue accent */
            letter-spacing: 1px;
            animation: titleSlide 1s ease-in-out;
        }

        /* Button cards */
        .btn-card {
            display: flex;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1ec6ff, #1b9ce6);
            padding: 18px;
            margin: 15px 0;
            border-radius: 15px;
            color: #fff;
            font-size: 18px;
            font-weight: 500;
            border: none;
            text-decoration: none;
            transition: transform 0.4s ease, box-shadow 0.4s ease;
            position: relative;
            overflow: hidden;
        }

        .btn-card::before {
            content: "";
            position: absolute;
            top: 0;
            left: -75%;
            width: 50%;
            height: 100%;
            background: rgba(255,255,255,0.2);
            transform: skewX(-25deg);
            transition: left 0.5s ease;
        }

        .btn-card:hover::before {
            left: 125%;
        }

        .btn-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(30,198,255,0.5);
        }

        /* Animations */
        @keyframes containerFade {
            from { opacity: 0; transform: scale(0.9); }
            to { opacity: 1; transform: scale(1); }
        }

        @keyframes titleSlide {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* Optional icons */
        .btn-card i {
            margin-right: 10px;
            font-size: 20px;
        }

    </style>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.css">
</head>
<body>
  {% include 'navbar.html' %}
<div class="dashboard-container">
   <h3>Wellcome {{Cust_Name}} !</h3>

  <a class="btn-card" href="{{url_for('Searchallproduct.Searchallproduct_index')}}">
    <i class="bi bi-search"></i>
    Search All Products
</a>

<a class="btn-card" href="/CustOrderRp">
    <i class="bi bi-graph-up-arrow"></i>
    My Orders
</a>


</div>

</body>
</html>

    """
    return render_template_string(html_string,Cust_Name=Cust_Name)


