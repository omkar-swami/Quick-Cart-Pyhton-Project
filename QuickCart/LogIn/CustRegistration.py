from flask import Flask, render_template_string, request,Blueprint,session,redirect,url_for
import pymysql

from companydashboard import companyDashboard_index

CustRegistration = Blueprint("CustRegistration",__name__)

def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid=0
    qry="SELECT MAX(Cust_Id) FROM customer"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid=i[0]
        if maxid is None:
            maxid="0"
        return int(maxid) + 1

@CustRegistration.route('/CustRegistration', methods=['GET', 'POST'])
def CustRegistration_index():
    conn = connection()
    cursor = conn.cursor()
    Cust_Id = GetNewID()
    if request.method == 'POST':
        Cust_Id = request.form['Cust_Id']
        Cust_Nm = request.form['Cust_Nm']
        Cust_Addr = request.form['Cust_Addr']
        Cust_Phone = request.form['Cust_Phone']
        Cust_Email = request.form['Cust_Email']
        Cust_Pincode = request.form['Cust_Pincode']
        Cust_Password = request.form['Cust_Password']
        cursor.execute("INSERT INTO customer VALUES (%s,%s,%s,%s,%s,%s,%s)",
                       (Cust_Id, Cust_Nm, Cust_Addr, Cust_Phone, Cust_Email, Cust_Pincode, Cust_Password))
        conn.commit()
        session["Cust_id"] = Cust_Id
        session['Cust_Name'] = Cust_Nm
        session['islogin'] = True
        session['role'] = 'Customer'
        return redirect(url_for('custdashboard.custdashboard_index'))
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <title>Create Account</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <script src="{{url_for('static',filename='js/ValidationLibrary.js')}}"></script>

  <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

  <style>
    body {
      background: linear-gradient(135deg, #e3f2fd, #bbdefb);
      font-family: 'Poppins', sans-serif;
      margin-top:110px;
    }

    /* Page container */
    .register-wrapper {
      display: flex;
      justify-content: center;
      padding-bottom: 60px;
    }

    /* Card */
    .register-card {
      width: 100%;
      max-width: 900px;
      background: #ffffff;
      border-radius: 20px;
      padding: 40px;
      box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
      animation: fadeIn 0.6s ease;
    }

    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(20px); }
      to { opacity: 1; transform: translateY(0); }
    }

    /* Heading */
    .register-title {
      text-align: center;
      font-weight: 700;
      color: #0d47a1;
      margin-bottom: 35px;
    }

    /* Inputs */
    .input-group {
      background: #f5faff;
      border-radius: 14px;
      overflow: hidden;
      border: 1px solid #cfd8dc;
      transition: 0.3s;
    }

    .input-group:hover {
      border-color: #2196f3;
      box-shadow: 0 0 10px rgba(33,150,243,0.25);
    }

    .input-group-text {
      background: transparent;
      border: none;
      color: #1976d2;
      font-size: 1.2rem;
      padding-left: 16px;
    }

    .form-control {
      border: none;
      background: transparent;
      padding: 14px;
      font-size: 1rem;
    }

    .form-control:focus {
      box-shadow: none;
    }

    /* Button */
    .btn-create {
      background: #ff9800;
      border: none;
      color: #fff;
      font-weight: 600;
      padding: 14px;
      border-radius: 14px;
      transition: 0.3s;
    }

    .btn-create:hover {
      background: #fb8c00;
      box-shadow: 0 10px 25px rgba(255,152,0,0.5);
      transform: translateY(-2px);
    }

    /* Back icon */
    .back-icon {
      font-size: 34px;
      color: #1976d2;
      transition: 0.3s;
    }

    .back-icon:hover {
      color: #0d47a1;
      transform: scale(1.1);
    }

    .login-link {
      color: #1976d2;
      font-weight: 500;
    }

    .login-link:hover {
      text-decoration: underline;
    }
  </style>
<script>
                    function formValidator() {            
                        var Cust_Nm = document.getElementById("txtCust_Nm");
                        var Cust_Addr = document.getElementById("txtCust_Addr");
                        var Cust_Phone=document.getElementById("txtCust_Phone");
                        var Cust_Email = document.getElementById("txtCust_Email");
                        var Cust_Pincode = document.getElementById("txtCust_Pincode");
                        var Cust_Password = document.getElementById("txtCust_Password");
                          
                                    
                        // Check each input in the order that it appears in the form!
                        if (notEmpty(Cust_Nm, "Name Must be given") && isAlphabet(Cust_Nm, "Please enter only letters for your name")) {
                             if (notEmpty(Cust_Addr, "Address Must be given") && isAlphanumeric(Cust_Addr, "Numbers and Letters Only for Address")) {
                                 if (notEmpty(Cust_Phone, "Mobile No Must be given") && validmobile(Cust_Phone) && isNumeric(Cust_Phone, "Please enter a valid Mobile no")) {
                                     if (notEmpty(Cust_Email, "Email Must be given") && emailValidator(Cust_Email, "Please enter a valid email address")) {
                                        if (notEmpty(Cust_Pincode,"Pincode Must be given")){
                                            if (notEmpty(Cust_Password,"enter a password") && isValidPassword(Cust_Password,"Enter a valid Password")){
                                                return true;    
                                            }
                                        }                                                 
                                     }
                                }
                            }
                        }                   
                     return false;
                    }
                </script>
</head>
<body>

{% include 'navbar.html' %}

<div class="register-wrapper">
  <div class="register-card">

    <a href="/CustLogin">
      <i class="bi bi-arrow-left-circle back-icon"></i>
    </a>

    <h2 class="register-title">Create Your Account</h2>

    <form method="POST" action="/CustRegistration" ">

      <div class="row g-4">

        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text">ID</span>
            <input type="text" class="form-control" name="Cust_Id" value="{{Cust_Id}}" readonly>
          </div>
        </div>

        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-person"></i></span>
            <input type="text" class="form-control" name="Cust_Nm" id="txtCust_Nm" placeholder="Full Name">
          </div>
        </div>

        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-telephone"></i></span>
            <input type="text" class="form-control" name="Cust_Phone" id="txtCust_Phone" placeholder="Mobile Number">
          </div>
        </div>

        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-envelope"></i></span>
            <input type="email" class="form-control" name="Cust_Email" id="txtCust_Email" placeholder="Email Address">
          </div>
        </div>

        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-geo-alt"></i></span>
            <input type="text" class="form-control" name="Cust_Pincode" id="txtCust_Pincode" placeholder="Pincode">
          </div>
        </div>

        <div class="col-12">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-house"></i></span>
            <input type="text" class="form-control" name="Cust_Addr" id="txtCust_Addr" placeholder="Full Address">
          </div>
        </div>

        <div class="col-12">
          <div class="input-group">
            <span class="input-group-text"><i class="bi bi-lock"></i></span>
            <input type="password" class="form-control" name="Cust_Password" id="txtCust_Password" placeholder="Create Password">
          </div>
        </div>

        <div class="col-12">
          <button type="submit" class="btn btn-create w-100" onclick="return formValidator()">
            Create Account
          </button>
        </div>

        <div class="col-12 text-center mt-2">
          <span>Already registered?
            <a href="/CustLogin" class="login-link">Login</a>
          </span>
        </div>

      </div>
    </form>

  </div>
</div>

</body>
</html>

    """
    return render_template_string(html_template,Cust_Id=Cust_Id )
