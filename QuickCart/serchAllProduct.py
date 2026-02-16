from flask import Flask, render_template_string, request,Blueprint
import pymysql
def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')
Searchallproduct = Blueprint('Searchallproduct', __name__)

@Searchallproduct.route("/Searchallproduct", methods=['GET', 'POST'])
def Searchallproduct_index():
    itemlist = []
    if request.method == 'GET':
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM itemmaster")
        itemlist = cursor.fetchall()
    cartMsg=request.args.get('cartMsg')

    html_string = """
     <!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Our Products</title>

<link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
<script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>
*{
  font-family: 'Poppins', sans-serif;
}

body{
  background: linear-gradient(120deg,#f4f7ff,#eef3ff);
  margin-top:110px;
  color:#1f2937;
}

/* ===== HEADER ===== */
.title{
  text-align:center;
  font-size:42px;
  font-weight:800;
  color:#1e40af;
}

.subtitle{
  text-align:center;
  font-size:17px;
  color:#64748b;
  margin-bottom:45px;
}

/* ===== PRODUCT CARD ===== */
.product-card{
  background: rgba(255,255,255,0.85);
  border-radius:22px;
  padding:18px;
  height:100%;
  transition:.35s ease;
  box-shadow:0 15px 40px rgba(0,0,0,0.08);
  border:1px solid rgba(0,0,0,0.04);
}

.product-card:hover{
  transform:translateY(-8px);
  box-shadow:0 25px 60px rgba(0,0,0,0.15);
}

/* ===== IMAGE ===== */
.image-box{
  height:260px;
  background:linear-gradient(135deg,#eaf2ff,#f6f9ff);
  border-radius:18px;
  display:flex;
  align-items:center;
  justify-content:center;
  overflow:hidden;
}

.image-box img{
  max-width:85%;
  max-height:85%;
  transition:.4s ease;
}

.product-card:hover img{
  transform:scale(1.07);
}

/* ===== TEXT ===== */
.product-title{
  margin-top:18px;
  font-size:22px;
  font-weight:700;
  color:#1e3a8a;
  text-align:center;
}

.price-text{
  font-size:20px;
  font-weight:700;
  color:#2563eb;
  text-align:center;
  margin-bottom:18px;
}

/* ===== BUTTONS ===== */
.btn-row{
  display:flex;
  gap:10px;
}

.btn-custom{
  flex:1;
  padding:10px 0;
  border-radius:30px;
  font-weight:600;
  background:#2563eb;
  color:#fff;
  text-decoration:none;
  text-align:center;
  transition:.3s ease;
}

.btn-custom.secondary{
  background:#e0ecff;
  color:#1e40af;
}

.btn-custom:hover{
  transform:translateY(-2px);
  box-shadow:0 10px 25px rgba(37,99,235,0.35);
}

.btn-custom.secondary:hover{
  background:#2563eb;
  color:#fff;
}

/* ===== OUT OF STOCK ===== */
.out-of-stock{
  margin-top:15px;
  background:#fff7ed;
  color:#9a3412;
  padding:14px;
  border-radius:14px;
  font-weight:600;
  text-align:center;
  font-size:14px;
  box-shadow:0 8px 20px rgba(0,0,0,0.08);
}

/* ===== CART POPUP ===== */
.cart-overlay{
  position:fixed;
  inset:0;
  background:rgba(0,0,0,0.55);
  display:flex;
  align-items:center;
  justify-content:center;
  z-index:9999;
}

.cart-msg-box{
  background:#fff;
  padding:35px;
  border-radius:22px;
  text-align:center;
  width:90%;
  max-width:380px;
  box-shadow:0 25px 60px rgba(0,0,0,0.25);
  animation:pop .35s ease;
}

@keyframes pop{
  from{transform:scale(.8);opacity:0}
  to{transform:scale(1);opacity:1}
}

.cart-msg-box p{
  font-size:20px;
  font-weight:700;
  color:#1e40af;
}

.cart-msg-box button{
  margin-top:20px;
  padding:10px 34px;
  border-radius:30px;
  border:none;
  background:#2563eb;
  color:#fff;
  font-weight:600;
}
</style>
</head>

<body>

{% include 'navbar.html' %}

<!-- CART MESSAGE -->
{% if cartMsg %}
<div class="cart-overlay" id="cartPopup">
  <div class="cart-msg-box">
    <p>{{ cartMsg }}</p>
    <button onclick="closePopup()">OK</button>
  </div>
</div>
{% endif %}

<div class="container pb-5">
  <h1 class="title">Our Featured Products</h1>
  <p class="subtitle">Hand-picked premium items curated for you</p>

  <div class="row g-4">
    {% for row in itemlist %}
    <div class="col-lg-4 col-md-6">
      <div class="product-card">

        <div class="image-box">
          <img src="{{ url_for('static', filename='uploads/' + row[8]) }}">
        </div>

        <h4 class="product-title">{{ row[1] }}</h4>
        <p class="price-text">₹ {{ row[5] }}</p>

        <div class="btn-row">
          {% if row[6] != 0 %}
          <a href="/addtocart?Item_Id={{ row[0] }}" class="btn-custom">
            Add to Cart
          </a>
          {% endif %}

          <a href="/ProductDetails?Item_Id={{ row[0] }}" class="btn-custom secondary">
            View Details
          </a>
        </div>

        {% if row[6] == 0 %}
        <div class="out-of-stock">
          Out of Stock<br>
          <small>Currently unavailable</small>
        </div>
        {% endif %}

      </div>
    </div>
    {% endfor %}
  </div>
</div>

<script>
function closePopup(){
  document.getElementById("cartPopup").style.display="none";
}
</script>

</body>
</html>



            """

    return render_template_string(html_string, itemlist=itemlist,cartMsg=cartMsg)
