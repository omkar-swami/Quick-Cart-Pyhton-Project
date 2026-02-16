from flask import Flask, render_template_string, Blueprint, request,session
import pymysql
from werkzeug.utils import redirect

addtocart = Blueprint('addtocart', __name__)
def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')
@addtocart.route("/addtocart", methods=['GET', 'POST'])
def addtocart_index():
    Item_Id = int(request.args.get('Item_Id'))


    conn = connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM itemmaster WHERE Item_Id=%s", (Item_Id,))
    itemlist = cursor.fetchall()
    conn.close()

    if not itemlist:
        return "Item Not Found"


    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]

    # 🔁 If already in cart
    for item in cart:
        if item["Item_id"] == Item_Id:
            item["Item_Qty"] += 1
            session.modified = True
            return redirect('/Searchallproduct?cartMsg=Item Added To Cart')

    # ➕ Add new item
    cart.append({
        "Item_id": itemlist[0][0],
        "Item_Nm": itemlist[0][1],
        "Comp_Id": itemlist[0][2],
        "Item_Rate": itemlist[0][5],
        "Item_Photo": itemlist[0][8],
        "Item_Qty": 1
    })

    session.modified = True
    return redirect('/Searchallproduct?cartMsg=Item Added To Cart')

