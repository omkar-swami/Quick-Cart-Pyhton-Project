from flask import Flask,render_template,session
from Brand import Brand
from Company import Company
from Customer import Customer
from Itemcategory import Itemcategory
from LogIn import ShopownerLogin
from Orderdetails import Orderdetails
from Itemmaster import Itemmaster
from OrderMaster import OrderMaster
from Payment import Payment


from ListReport.Brandlist import Brandlist
from ListReport.Companylist import Companylist
from ListReport.Customerlist import Customerlist
from ListReport.Itemcategorylist import Itemcategorylist
from ListReport.Itemmasterlist import Itemmasterlist
from ListReport.Orderdetailslist import Orderdetailslist
from ListReport.OrderMasterlist import OrderMasterlist
from ListReport.Paymentlist import Paymentlist

from DynamicReport.BrandwiseItemmaster import BrandwiseItemmaster
from DynamicReport.CompanywiseItemmaster import CompanywiseItemmaster
from DynamicReport.ItemcatwiseItemmaster import ItemcatwiseItemmaster
# from DynamicReport.CompanywiseOrdermaster import CompanywiseOrdermaster
from DynamicReport.CompanywiseOrderDetails import CompanywiseOrderDetails
from DynamicReport.CustomerwiseOrdermaster import CustomerwiseOrdermaster
from DynamicReport.OrderMasterwisePayment import OrderMasterwisePayment
from DynamicReport.OrderMasterwiseOrderdetails import OrderMasterwiseOrderdetails
from DynamicReport.ItemMasterwiseOrderdetails import ItemMasterwiseOrderdetails

from DatewiseReport.DatewiseOrderMaster import DatewiseOrderMaster
from DatewiseReport.DatewisePayment import DatewisePayment


from LogIn.AdminLogin import AdminLogin
from LogIn.CustomerLogin import CustLogin
from LogIn.ShopownerLogin import shopOwnerLogin

from AdminDashboard import AdminDashboard
from CustomerDashboard import custdashboard
from companydashboard import  companyDashboard

from serchAllProduct import Searchallproduct
from productDetails import ProductDetails

from datetime import timedelta
from AddToCart import  addtocart
from ShowCart import showcart
from LogOut import logout
from  CheckOut import checkout
from Invoice import Invoice
from CustOrderRp import CustOrderRp
from CompanyWiseOrderInfo import CompanyWiseOrderInfo
from LogIn.CustRegistration import CustRegistration
from LogIn.ShopRegistration import ShopRegistration
app=Flask(__name__)

app.secret_key="SoftTech#2011"
app.permanent_session_lifetime = timedelta(hours=12)


app.register_blueprint(Brand)
app.register_blueprint(Company)
app.register_blueprint(Customer)
app.register_blueprint(Itemcategory)
app.register_blueprint(Orderdetails)
app.register_blueprint(Itemmaster)
app.register_blueprint(OrderMaster)
app.register_blueprint(Payment)

app.register_blueprint(Brandlist)
app.register_blueprint(Companylist)
app.register_blueprint(Customerlist)
app.register_blueprint(Itemcategorylist)
app.register_blueprint(Itemmasterlist)
app.register_blueprint(Orderdetailslist)
app.register_blueprint(OrderMasterlist)
app.register_blueprint(Paymentlist)

app.register_blueprint(BrandwiseItemmaster)
app.register_blueprint(CompanywiseItemmaster)
app.register_blueprint(ItemcatwiseItemmaster)
app.register_blueprint(CompanywiseOrderDetails)
app.register_blueprint(CustomerwiseOrdermaster)
app.register_blueprint(OrderMasterwisePayment)
app.register_blueprint(OrderMasterwiseOrderdetails)
app.register_blueprint(ItemMasterwiseOrderdetails)


app.register_blueprint(DatewiseOrderMaster)
app.register_blueprint(DatewisePayment)


app.register_blueprint(AdminLogin)
app.register_blueprint(CustLogin)
app.register_blueprint(shopOwnerLogin)

app.register_blueprint(AdminDashboard)
app.register_blueprint(custdashboard)
app.register_blueprint(companyDashboard)

app.register_blueprint(Searchallproduct)
app.register_blueprint(ProductDetails)
app.register_blueprint(addtocart)
app.register_blueprint(showcart)
app.register_blueprint(checkout)
app.register_blueprint(logout)
app.register_blueprint(Invoice)
app.register_blueprint(CustOrderRp)

app.register_blueprint(CustRegistration)
app.register_blueprint(CompanyWiseOrderInfo)
app.register_blueprint(ShopRegistration)

@app.route("/")
def index():
     return render_template('Home.html')
if __name__ == '__main__':
    app.run(debug=True,port=5005)

