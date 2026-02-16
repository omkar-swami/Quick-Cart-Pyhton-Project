from flask import Flask, render_template_string, request,Blueprint
import pymysql
def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')
ProductDetails = Blueprint('ProductDetails', __name__)

@ProductDetails.route("/ProductDetails", methods=['GET', 'POST'])
def ProductDetails_index():
    itemlist = []
    if request.method == 'GET':
        conn = connection()
        cursor = conn.cursor()
        Item_Id = request.args.get('Item_Id')
        cursor.execute("SELECT * FROM itemmaster where Item_Id=%s", (Item_Id,))
        itemlist = cursor.fetchall()
    html_string="""
      <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Product Details</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

    <style>
        body {
            background: linear-gradient(120deg, #e8f1ff, #f5f9ff);
            font-family: 'Poppins', sans-serif;
            color: #1b1b1b;
            padding: 40px 0;
            margin-top:40px;
        }

        .product-container {
            display: flex;
            justify-content: center;
            margin: 50px auto;
            max-width: 1150px;
        }

        .product-card {
            display: flex;
            background: #ffffff;
            width: 100%;
            border-radius: 20px;
            overflow: hidden;
            padding: 15px;
            border: 1px solid #b8d4ff;
            
            transition: 0.4s ease-in-out;
        }

        .product-card:hover {
            transform: translateY(-10px);
            border-color: #3a7bff;
        }

        .product-left {
            flex: 1;
            padding: 35px;
            
            border-radius: 18px;
        }

        /* Title */
   .product-left h2 {
    font-size: 35px;
    font-weight: 800;
    color: #005eff;
    margin-bottom: 18px;
}


        /* Back Button */
        .back-btn {
            display: inline-block;
            background: linear-gradient(90deg, #3a7bff, #5c9cff);
            color: #fff;
            padding: 10px 28px;
            border-radius: 10px;
            font-weight: 600;
            text-decoration: none;
            box-shadow: 0 6px 18px rgba(60, 110, 255, 0.4);
            transition: 0.3s;
            font-size: 15px;
            margin-bottom: 20px;
        }

        .back-btn:hover {
            transform: scale(1.07);
            background: #5b8cff;
        }

        .details p {
            font-size: 16px;
            margin: 8px 0;
            letter-spacing: .3px;
            color: #333;
        }

        .details b {
            color: #005eff;
            font-weight: 600;
        }

        /* Price */
        .price-block {
            margin-top: 25px;
        }

        .price-title {
            color: #555;
            font-size: 17px;
        }

        .price-value {
            font-size: 45px;
            font-weight: 800;
            color: #005eff;
            text-shadow: 0 0 8px rgba(0, 119, 255, 0.3);
        }

        /* Buttons */
        .action-buttons {
            margin-top: 30px;
            display: flex;
            gap: 20px;
        }

        .action-buttons a {
            padding: 12px 35px;
            font-size: 17px;
            font-weight: 600;
            border-radius: 10px;
            text-decoration: none;
            transition: .3s ease;
        }

        .buy-btn {
            background: linear-gradient(90deg, #005eff, #0090ff);
            color: white;
            box-shadow: 0 6px 20px rgba(0, 96, 255, 0.3);
        }

        .buy-btn:hover {
            background: #006bff;
            transform: translateY(-3px);
        }

        .cart-btn {
            background: transparent;
            border: 2px solid #005eff;
            color: #005eff;
        }

        .cart-btn:hover {
            background: #005eff;
            color: white;
            transform: translateY(-3px);
        }

        /* RIGHT SIDE */
        .product-right {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #f1f6ff;
            border-radius: 18px;
            padding: 30px;
        }

        .product-right img {
            width: 100%;
            max-width: 480px;
            height:450px;
          box-shadow:2px 3px 20px black;
            transition: .5s;
        }

        .product-right img:hover {
            transform: scale(1.05);
            box-shadow:7px 7px 20px black;
        }
          .out-of-stock {
    background: #fff3cd;
    color: #856404;
    border: 1px solid #ffeeba;
    margin-top: 10px;
    margin-left:25px;
    padding: 12px 16px;
    border-radius: 8px;
    font-weight: 600;
    display: inline-block;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
}

.out-of-stock span {
    display: block;
    font-size: 14px;
    font-weight: normal;
    margin-top: 4px;
}
    </style>
</head>

<body>
  {% include 'navbar.html' %}
{% for row in itemlist %}
<div class="product-container">
    <div class="product-card">

        <!-- LEFT -->
        <div class="product-left">

            <a href="{{ url_for('Searchallproduct.Searchallproduct_index') }}" class="back-btn">← Back</a>

            <h2 id="title"><strong>{{ row[1] }}</strong></h2>


            <div class="details">
                <p><b>Company:</b> {{ row[2] }}</p>
                <p><b>Category:</b> {{ row[3] }}</p>
                <p><b>Brand:</b> {{ row[4] }}</p>
                <p><b>Description:</b> {{ row[7] }}</p>
            </div>

            <div class="price-block">
                <p class="price-title">Price</p>
                <p class="price-value">₹{{ row[5] }}</p>
            </div>

            <div class="action-buttons">
              
                <a  href="/addtocart?Item_Id={{ row[0] }}"  class="cart-btn"  {% if row[6]==0 %} style="display: None" {% endif %}>Add to Cart</a>
            </div>
   {% if row[6]==0 %} 
                  <div class="out-of-stock">
                            Out of Stock  
                            <span>Currently unavailable. Please check back later.</span>
                     </div>
                 {% endif %}
        </div>

        <!-- RIGHT -->
        <div class="product-right">
            <img src="{{ url_for('static', filename='uploads/' + row[8]) }}">
        </div>

    </div>
</div>
{% endfor %}

</body>
</html>


        """
    return  render_template_string(html_string,itemlist=itemlist)
