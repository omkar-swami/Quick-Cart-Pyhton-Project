from flask import Flask, render_template_string, Blueprint, request, redirect, url_for,session
import pymysql
ShopRegistration = Blueprint('ShopRegistration', __name__)


def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')


def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid = 0
    qry = "SELECT MAX(Comp_Id) FROM company"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid = i[0]
        if maxid is None:
            maxid = "0"
        return int(maxid) + 1

@ShopRegistration.route("/ShopRegistration", methods=['GET', 'POST'])
def ShopRegistration_index():
    Comp_Id = GetNewID()
    if request.method == 'POST':
        Comp_Id = request.form['Comp_Id']
        Comp_Nm = request.form['Comp_Nm']
        Comp_Addr = request.form['Comp_Addr']
        Comp_Phone = request.form['Comp_Phone']
        Comp_Email = request.form['Comp_Email']
        Comp_City = request.form['Comp_City']
        Comp_Descr = request.form['Comp_Descr']
        Comp_Password = request.form['Comp_Password']
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO company VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
                       (Comp_Id, Comp_Nm, Comp_Addr, Comp_Phone, Comp_Email, Comp_City, Comp_Descr, Comp_Password))
        conn.commit()
        session['Comp_id'] = Comp_Id
        session['Comp_nm'] = Comp_Nm
        session['islogin'] = True
        session['role'] = 'ShopOwner'
        return redirect(url_for('companyDashboard.companyDashboard_index'))
    html_template = """<<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Shop Registration</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

    <!-- Validation JS -->
    <script src="{{url_for('static',filename='js/ValidationLibrary.js')}}"></script>

    <style>
        body {
            background: linear-gradient(120deg, #eef2f7, #dbe7f3);
            font-family: 'Segoe UI', sans-serif;
            margin-top: 40px;
        }

        .register-card {
            max-width: 900px;
            margin: 50px auto;
            background: #ffffff;
            padding: 40px;
            border-radius: 14px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }

        .register-card h2 {
            text-align: center;
            margin-bottom: 30px;
            font-weight: 600;
            color: #1f3c88;
        }

        /* 2-column layout */
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 22px;
            margin-bottom: 22px;
        }

        /* Single column */
        .form-group {
            position: relative;
        }

        .form-group input {
            width: 100%;
            padding: 14px 12px;
            border: 1px solid #cfd8dc;
            border-radius: 8px;
            font-size: 15px;
            outline: none;
            background: transparent;
            transition: all 0.3s ease;
        }

        .form-group input:focus {
            border-color: #1f3c88;
            box-shadow: 0 0 0 3px rgba(31,60,136,0.15);
        }

        .form-group label {
            position: absolute;
            top: 50%;
            left: 12px;
            color: #777;
            font-size: 14px;
            transform: translateY(-50%);
            pointer-events: none;
            background: #fff;
            padding: 0 6px;
            transition: 0.3s ease;
        }

        .form-group input:focus + label,
        .form-group input:not(:placeholder-shown) + label {
            top: -7px;
            font-size: 12px;
            color: #1f3c88;
        }

        input[readonly] {
            background: #f1f3f5;
            cursor: not-allowed;
        }

        .submit-btn {
            width: 100%;
            padding: 14px;
            border-radius: 10px;
            border: none;
            background: linear-gradient(135deg, #1f3c88, #3f72af);
            color: #fff;
            font-size: 16px;
            font-weight: 500;
            transition: 0.3s ease;
        }

        .submit-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(31,60,136,0.3);
        }

        /* Mobile view */
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
            }
        }
    </style>

    <script>
        function formValidator() {            
            var Comp_Nm = document.getElementById("txtComp_Nm");
            var Comp_Addr = document.getElementById("txtComp_Addr");
            var Comp_Phone = document.getElementById("txtComp_Phone");
            var Comp_Email = document.getElementById("txtComp_Email");
            var Comp_City = document.getElementById("txtComp_City");
            var Comp_Descr = document.getElementById("txtComp_Descr");
            var Comp_Password = document.getElementById("txtComp_Password");

            if (notEmpty(Comp_Nm, "Name Must be given") && isAlphabet(Comp_Nm)) {
                if (notEmpty(Comp_Addr, "Address Must be given")) {
                    if (notEmpty(Comp_Phone, "Mobile No Must be given") && validmobile(Comp_Phone)) {
                        if (notEmpty(Comp_Email, "Email Must be given") && emailValidator(Comp_Email)) {
                            if (notEmpty(Comp_City,"City Must be given")) {
                                if (notEmpty(Comp_Descr,"Description Must be given")) {
                                    if (notEmpty(Comp_Password,"Password Required") && isValidPassword(Comp_Password)) {
                                        return true;
                                    }
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

<div class="register-card">
    <h2>Shop Registration</h2>

    <form method="POST" action="/ShopRegistration">

        <!-- Row 1 -->
        <div class="form-row">
            <div class="form-group">
                <input type="text" name="Comp_Id" value="{{ Comp_Id }}" readonly placeholder=" ">
                <label>Company ID</label>
            </div>

            <div class="form-group">
                <input type="text" name="Comp_Nm" id="txtComp_Nm" value="{{ Comp_Nm }}" placeholder=" ">
                <label>Company Name</label>
            </div>
        </div>

        <!-- Row 2 -->
        <div class="form-row">
            <div class="form-group">
                <input type="text" name="Comp_Phone" id="txtComp_Phone" value="{{ Comp_Phone }}" placeholder=" ">
                <label>Phone Number</label>
            </div>

            <div class="form-group">
                <input type="text" name="Comp_Email" id="txtComp_Email" value="{{ Comp_Email }}" placeholder=" ">
                <label>Email Address</label>
            </div>
        </div>

        <!-- Row 3 -->
        <div class="form-row">
            <div class="form-group">
                <input type="text" name="Comp_City" id="txtComp_City" value="{{ Comp_City }}" placeholder=" ">
                <label>City</label>
            </div>

            <div class="form-group">
                <input type="password" name="Comp_Password" id="txtComp_Password" value="{{ Comp_Password }}" placeholder=" ">
                <label>Password</label>
            </div>
        </div>

        <!-- Full width -->
        <div class="form-group mb-4">
            <input type="text" name="Comp_Addr" id="txtComp_Addr" value="{{ Comp_Addr }}" placeholder=" ">
            <label>Company Address</label>
        </div>

        <div class="form-group mb-4">
            <input type="text" name="Comp_Descr" id="txtComp_Descr" value="{{ Comp_Descr }}" placeholder=" ">
            <label>Description</label>
        </div>

        <button type="submit" class="submit-btn" onclick="return formValidator()">Register Shop</button>
    </form>
</div>

</body>
</html>


    """
    return render_template_string(html_template,Comp_Id=Comp_Id
                                )

