from flask import Blueprint, session, render_template_string, request, redirect, url_for, render_template
import  pymysql

showcart = Blueprint('showcart', __name__)
def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

@showcart.route("/showcart", methods=["GET", "POST"])
def showcart_index():

    # Get cart from session
    cart=[]

    if "cart" in session:
        cart = session["cart"]
    stock_Error = request.args.get('stock_Error')
    # ---------------- FORM ACTION HANDLING ----------------
    if request.method == "POST":
        btn = request.form.get("btn")
        Item_id =int(request.form.get("Item_id"))
        conn = connection()
        cursor = conn.cursor()
        itemlist=[]
        cursor.execute("SELECT * FROM itemmaster where Item_Id=%s", (Item_id,))
        itemlist = cursor.fetchall()

        for item in cart:
            if item["Item_id"] == Item_id:

                if btn == "Increase":
                    if item["Item_Qty"]< itemlist[0][6]:
                        item["Item_Qty"] += 1
                    else:
                        stock_Error=f"the stock {itemlist[0][1]} is {itemlist[0][6]} so you can  order maximum {itemlist[0][6]} items"
                        return redirect(url_for('showcart.showcart_index',stock_Error=stock_Error))



                elif btn == "Decrease":
                    if item["Item_Qty"] > 1:
                        item["Item_Qty"] -= 1

                elif btn == "Remove":
                    cart.remove(item)
                break

        session["cart"] = cart
        return redirect(url_for('showcart.showcart_index'))

    # ---------------- CALCULATE TOTAL ----------------
    grand_total = 0
    for item in cart:
        item["total"] = item["Item_Qty"] * item["Item_Rate"]
        grand_total += item["total"]

    # ---------------- HTML TEMPLATE ----------------
    html_string = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Cart</title>

    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">

    <style>
        body{
            background:#f5f7fa;
            margin-top:110px;
            font-family: "Segoe UI", Roboto, Arial, sans-serif;
        }

        .cart-container{
            max-width:1100px;
            margin:auto;
        }

        .cart-card{
            background:#ffffff;
            border-radius:8px;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
            padding:25px;
        }

        .cart-title{
            font-size:26px;
            font-weight:600;
            color:#0d6efd;
            margin-bottom:25px;
        }

        .cart-img{
            width:70px;
            height:70px;
            object-fit:contain;
            border:1px solid #dee2e6;
            border-radius:6px;
            padding:4px;
            background:#fff;
        }

        table th{
            font-weight:600;
            color:#495057;
            background:#f8f9fa;
            border-bottom:2px solid #dee2e6;
            text-align:center;
        }

        table td{
            vertical-align:middle;
            color:#212529;
        }

        .qty-badge{
            background:#e9ecef;
            color:#212529;
            padding:6px 14px;
            border-radius:20px;
            font-weight:500;
        }

        .btn-sm{
            padding:4px 10px;
            font-size:13px;
        }

        .cart-total{
            border-top:1px solid #dee2e6;
            margin-top:20px;
            padding-top:15px;
            text-align:right;
            font-size:20px;
            font-weight:600;
            color:#198754;
        }

        .cart-actions{
            margin-top:25px;
            text-align:right;
        }

        .cart-actions a{
            min-width:180px;
            padding:10px 16px;
            font-weight:500;
        }

        .empty-cart{
            background:#ffffff;
            padding:40px;
            border-radius:8px;
            text-align:center;
            box-shadow:0 4px 12px rgba(0,0,0,0.08);
        }
    </style>
</head>

<body>

{% include 'navbar.html' %}

<div class="container cart-container">

    <div class="cart-card">

        <div class="cart-title">Shopping Cart</div>
        {% if stock_Error %}
            <p style="color:red;"> {{stock_Error}}</p>
        {% endif %}
        {% if cart %}
        <table class="table align-middle">
            <thead>
                <tr>
                    <th width="10%">Product</th>
                    <th width="25%">Name</th>
                    <th width="15%">Price</th>
                    <th width="10%">Quantity</th>
                    <th width="25%">Actions</th>
                    <th width="15%">Total</th>
                </tr>
            </thead>

            <tbody>
            {% for item in cart %}
                <tr>
                    <td>
                        <img src="{{ url_for('static', filename='uploads/' + item['Item_Photo']) }}"
                             class="cart-img" alt="Product Image">
                    </td>

                    <td>{{ item['Item_Nm'] }}</td>

                    <td>₹ {{ item['Item_Rate'] }}</td>

                    <td>
                        <span class="qty-badge">{{ item['Item_Qty'] }}</span>
                    </td>

                    <td>
                        <form method="post" action="/showcart" class="d-inline">
                            <input type="hidden" name="Item_id" value="{{ item['Item_id'] }}">

                            <button type="submit" name="btn" value="Increase"
                                    class="btn btn-outline-success btn-sm">
                                +
                            </button>

                            <button type="submit" name="btn" value="Decrease"
                                    class="btn btn-outline-warning btn-sm">
                                -
                            </button>

                            <button type="submit" name="btn" value="Remove"
                                    class="btn btn-outline-danger btn-sm"
                                    onclick="return confirm('Remove this item from cart?')">
                                Remove
                            </button>
                        </form>
                    </td>

                    <td class="fw-semibold">
                        ₹ {{ item['total'] }}
                    </td>
                </tr>
            {% endfor %}
            </tbody>
        </table>

        <div class="cart-total">
            Grand Total : ₹ {{ grand_total }}
        </div>

        <div class="cart-actions">
            <a href="/Searchallproduct" class="btn btn-outline-secondary me-2">
                Continue Shopping
            </a>
            <a href="/checkout" class="btn btn-success">
                Proceed to Checkout
            </a>
        </div>

        {% else %}
        <div class="empty-cart">
            <h5 class="text-muted mb-3">Your shopping cart is empty</h5>
            <a href="/Searchallproduct" class="btn btn-primary">
                Browse Products
            </a>
        </div>
        {% endif %}

    </div>

</div>

</body>
</html>

"""

    return render_template_string(
        html_string,
        cart=cart,
        grand_total=grand_total,
    stock_Error=stock_Error
    )
