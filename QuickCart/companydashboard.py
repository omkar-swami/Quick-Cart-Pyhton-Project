from flask import Flask, render_template_string, Blueprint, session

companyDashboard = Blueprint('companyDashboard', __name__)


@companyDashboard.route("/companyDashboard", methods=['GET', 'POST'])
def companyDashboard_index():
    Comp_nm=''
    if 'Comp_nm' in session:
        Comp_nm=session['Comp_nm']

    html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Company Dashboard</title>

<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
<script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

<style>
body{
    margin-top:100px;
    background:
        radial-gradient(circle at top, #1b2b4a, #0f172a);
    font-family: "Segoe UI", sans-serif;
    color:#fff;
}

/* Page container */
.dashboard-container{
    max-width:1200px;
    margin:auto;
    padding:30px;
}

/* Header */
.dashboard-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:40px;
}

.dashboard-header h2{
    font-weight:700;
    letter-spacing:0.5px;
}

.dashboard-header span{
    color:#93c5fd;
    font-size:14px;
}

/* Cards */
.dashboard-card{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(14px);
    border-radius:18px;
    padding:30px 25px;
    box-shadow:0 15px 40px rgba(0,0,0,0.4);
    transition:0.35s ease;
    position:relative;
    overflow:hidden;
    height:100%;
}

.dashboard-card::before{
    content:"";
    position:absolute;
    top:0;
    left:-100%;
    width:100%;
    height:100%;
    background:linear-gradient(120deg, transparent, rgba(255,255,255,0.25), transparent);
    transition:0.5s;
}

.dashboard-card:hover::before{
    left:100%;
}

.dashboard-card:hover{
    transform:translateY(-10px) scale(1.02);
    box-shadow:0 25px 60px rgba(59,130,246,0.45);
}

/* Icon */
.card-icon{
    width:60px;
    height:60px;
    display:flex;
    align-items:center;
    justify-content:center;
    border-radius:16px;
    font-size:30px;
    margin-bottom:20px;
}

.products{ background:linear-gradient(135deg,#22c55e,#16a34a); }
.orders{ background:linear-gradient(135deg,#3b82f6,#2563eb); }
.payments{ background:linear-gradient(135deg,#f59e0b,#d97706); }
.profile{ background:linear-gradient(135deg,#ec4899,#be185d); }

/* Text */
.dashboard-card h5{
    font-weight:600;
    margin-bottom:10px;
}

.dashboard-card p{
    font-size:14px;
    color:#cbd5f5;
    margin-bottom:20px;
}

/* Button */
.dashboard-card a{
    display:inline-block;
    padding:8px 18px;
    border-radius:30px;
    font-size:14px;
    font-weight:600;
    text-decoration:none;
    background:rgba(255,255,255,0.15);
    color:#fff;
    transition:0.3s;
}

.dashboard-card a:hover{
    background:#fff;
    color:#111827;
}

/* Footer text */
.footer-note{
    text-align:center;
    margin-top:50px;
    font-size:13px;
    color:#94a3b8;
}
</style>
</head>

<body>

{% include 'navbar.html' %}

<div class="dashboard-container">

    <div class="dashboard-header">
        <div>
            <h2>{{Comp_nm}}</h2>
            <span>Manage your business efficiently</span>
        </div>
    </div>

    <div class="row g-4">

        <div class="col-md-3">
            <div class="dashboard-card">
                <div class="card-icon products">📦</div>
                <h5>Manage Products</h5>
                <p>Add, edit, and organize your product catalog</p>
                <a href="/itemmaster">Open →</a>
            </div>
        </div>

        <div class="col-md-3">
            <div class="dashboard-card">
                <div class="card-icon orders">🛒</div>
                <h5>View Orders</h5>
                <p>Track orders, shipping, and order status</p>
                <a href="/CompanyWiseOrderInfo">Open →</a>
            </div>
        </div>

        <div class="col-md-3">
    <div class="dashboard-card">
        <div class="card-icon orders">📅</div>
        <h5>Date Wise Orders</h5>
        <p>View and analyze orders based on selected dates</p>
        <a href="/datewiseOrderMaster">Open →</a>
    </div>
</div>


       

    </div>

    <div class="footer-note">
        © 2026 {{Comp_nm}} • Premium Admin UI
    </div>

</div>

</body>
</html>


    """
    return render_template_string(html_template,Comp_nm=Comp_nm)