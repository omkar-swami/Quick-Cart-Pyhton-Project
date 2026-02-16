from flask import Flask, render_template_string, Blueprint, request, redirect, url_for, session

AdminLogin = Blueprint('AdminLogin', __name__)

@AdminLogin.route("/AdminLogin", methods=['GET', 'POST'])
def AdminLogin_index():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == '123':
            session['islogin'] = True
            session['role'] = 'Admin'
            return redirect(url_for('AdminDashboard.AdminDashboard_index'))
        else:
            error = "Invalid username or password"

    html_string = """
     <!DOCTYPE html>
<html lang="en">
<head>
  <title>Customer Login</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">

  <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

  <style>
    body {
      margin: 0;
      padding: 0;
      height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #e3f2fd, #bbdefb);
      font-family: 'Poppins', sans-serif;
    }

    /* Login Card */
    .login-card {
      width: 100%;
      max-width: 420px;
      padding: 30px;
      background: #ffffff;
      border-radius: 16px;
      color: #0d47a1;
      border: 1px solid #90caf9;
      box-shadow: 0px 8px 25px rgba(33, 150, 243, 0.3);
      animation: fadeIn 0.6s ease-in-out;
    }

    /* Animation */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    /* Heading */
    .login-card h4 {
      text-align: center;
      margin-bottom: 25px;
      color: #0d47a1;
      font-weight: bold;
      font-size: 2rem;
    }

    /* Inputs */
    .form-control {
      background-color: #e3f2fd;
      border: 1px solid #64b5f6;
      color: #0d47a1;
      padding: 12px;
      border-radius: 10px;
      transition: 0.3s;
    }

    .form-control::placeholder {
      color: #0d47a1b7;
    }

    .form-control:focus {
      background-color: #bbdefb;
      border-color: #1976d2;
      color: #0d47a1;
      box-shadow: 0 0 12px rgba(25, 118, 210, 0.5);
    }

    /* Button */
    .btn-primary {
      background-color: #1976d2;
      border: none;
      color: #fff;
      font-weight: bold;
      padding: 12px;
      border-radius: 10px;
      transition: 0.3s;
    }

    .btn-primary:hover {
      background-color: #0d47a1;
      box-shadow: 0 0 15px rgba(13, 71, 161, 0.6);
    }

    /* Back Icon */
    .back-icon {
      font-size: 40px;
      color: #0d47a1;
      cursor: pointer;
      margin-bottom: 10px;
      transition: 0.3s;
    }

    .back-icon:hover {
      color: #1976d2;
    }

    .error-message {
      margin-top: 10px;
      color: #d32f2f;
      text-align: center;
      font-weight: bold;
    }
  </style>

</head>
<body>

  {% include 'navbar.html' %}

  <div class="login-card">
    <a href="{{ url_for('index') }}">
      <i class="bi bi-arrow-left-circle back-icon"></i>
    </a>

    <h4>Admin Login</h4>

    <form action="/AdminLogin" method="POST">
      <div class="mb-3">
        <input type="text" class="form-control" placeholder="User name" required name='username'/>
      </div>

      <div class="mb-3">
        <input type="password" class="form-control" placeholder="Password" required name='password'/>
      </div>

      <button type="submit" class="btn btn-primary w-100">Login</button>

      {% if error %}
        <p class="error-message">{{ error }}</p>
      {% endif %}
    </form>
  </div>

</body>
</html>

    """
    return render_template_string(html_string, error=error)


