from flask import Flask, render_template_string, request, Blueprint, session
import pymysql
import  os
Itemmaster = Blueprint("Itemmaster",__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
def connection():
    return pymysql.connect(host='localhost', user='root', password='', database='quickcart')

def GetNewID():
    conn = connection()
    cursor = conn.cursor()
    maxid=0
    qry="SELECT MAX(Item_Id) FROM itemmaster"
    cursor.execute(qry)
    rs = cursor.fetchall()
    for i in rs:
        maxid=i[0]
        if maxid is None:
            maxid="0"
        return int(maxid) + 1

def clear_textbox():
    return '', '', '', '', '', '', '', '', ''

@Itemmaster.route('/itemmaster', methods=['GET', 'POST'])
def Itemmaster_index():
    item_list=[]
    comp_list=[]
    cat_list=[]
    brand_list = []
    Item_Id=''
    Item_Nm=''
    Comp_Id=''
    Cat_Id=''
    Brand_Id=''
    Item_Rate=''
    Item_Stock=''
    Item_Descr=''
    Item_Photo=''
    role=""
    if 'role' in session:
        role=session['role']
    Item_Id = request.args.get('Item_Id', '')
    Item_Nm = request.args.get('Item_Nm', '')
    Comp_Id = request.args.get('Comp_Id', '')
    Cat_Id = request.args.get('Cat_Id', '')
    Brand_Id = request.args.get('Brand_Id', '')
    Item_Rate = request.args.get('Item_Rate','')
    Item_Stock=request.args.get('Item_Stock','')
    Item_Descr=request.args.get('Item_Descr','')
    Item_Photo=request.args.get('Item_Photo')
    is_record = bool(Item_Id)

    if not is_record:
        Item_Id = GetNewID()

    if request.method == 'POST':
        btn = request.form['btn']
        conn = connection()
        cursor = conn.cursor()
        try:
            Item_Id = request.form['Item_Id']
            Item_Nm = request.form['Item_Nm']
            Comp_Id = request.form['Comp_Id']
            Cat_Id = request.form['Cat_Id']
            Brand_Id = request.form['Brand_Id']
            Item_Rate = request.form['Item_Rate']
            Item_Stock = request.form['Item_Stock']
            Item_Descr = request.form['Item_Descr']
            Item_Photo = request.files.get('Item_Photo')
            photo_nm = ""
            if Item_Photo and Item_Photo.filename:
                photo_nm =Item_Id+"_"+ Item_Photo.filename
                file_path = os.path.join(UPLOAD_FOLDER, photo_nm)
                Item_Photo.save(file_path)

            if btn == 'Insert':
                cursor.execute("INSERT INTO itemmaster VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Item_Id, Item_Nm,Comp_Id,Cat_Id,Brand_Id,Item_Rate,Item_Stock,Item_Descr,str(photo_nm)))
                conn.commit()
                Item_Id, Item_Nm, Comp_Id, Cat_Id, Brand_Id, Item_Rate, Item_Stock, Item_Descr, Item_Photo = clear_textbox()
                Item_Id = GetNewID()
                is_record = False

            elif btn == 'Update':
                cursor.execute("UPDATE itemmaster SET Item_Nm=%s,Comp_Id=%s,Cat_Id=%s,Brand_Id=%s,Item_rate=%s,Item_Stock=%s,Item_Descr=%s,Item_Photo=%s WHERE Item_Id=%s", (Item_Nm,Comp_Id,Cat_Id,Brand_Id,Item_Rate,Item_Stock,Item_Descr,str(photo_nm),Item_Id,))
                conn.commit()
                Item_Id, Item_Nm,Comp_Id,Cat_Id,Brand_Id,Item_Rate,Item_Stock,Item_Descr,Item_Photo = clear_textbox()
                Item_Id = GetNewID()
                is_record = False

            elif btn == 'Delete':
                cursor.execute("DELETE FROM itemmaster WHERE Item_Id=%s", (Item_Id,))
                conn.commit()
                Item_Id, Item_Nm,Comp_Id,Cat_Id,Brand_Id,Item_Rate,Item_Stock,Item_Descr,Item_Photo = clear_textbox()
                Item_Id = GetNewID()
                is_record = False

        except Exception as e:
            print (e)

    conn = connection()
    cursor = conn.cursor()

    if role=='Admin':
        cursor.execute("SELECT * FROM itemmaster")
        Item_list = cursor.fetchall()
    if role=='ShopOwner':
        Comp_Id=session['Comp_id']
        cursor.execute("SELECT * FROM itemmaster where Comp_Id=%s", (Comp_Id,))
        Item_list = cursor.fetchall()


    cursor.execute("SELECT * FROM company")
    comp_list = cursor.fetchall()
    cursor.execute("SELECT * FROM itemcat")
    cat_list = cursor.fetchall()
    cursor.execute("SELECT * FROM brand")
    brand_list = cursor.fetchall()
    cursor.close()
    conn.close()


    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Item Master</title>

    <!-- Bootstrap -->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
    <script src="{{ url_for('static', filename='js/bootstrap.bundle.min.js') }}"></script>

    <!-- Validation -->
    <script src="{{url_for('static',filename='js/ValidationLibrary.js')}}"></script>

    <!-- Custom Styling -->
    <style>
        body {
            background: #f4f6f9;
            font-family: 'Poppins', sans-serif;
        }

        .page-title {
            font-weight: 700;
            color: #0d6efd;
            text-align: center;
            margin-bottom: 30px;
        }

        .card {
            border: none;
            border-radius: 16px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.08);
        }

        .form-label {
            font-weight: 500;
        }

        .form-control, .form-select {
            border-radius: 10px;
        }

        .btn {
            border-radius: 10px;
            padding: 8px 18px;
        }

        table {
            border-radius: 14px;
            overflow: hidden;
        }

        thead {
            background: #0d6efd;
            color: white;
        }

        tbody tr:hover {
            background-color: #f1f5ff;
        }
    </style>

    <!-- Form Validation -->
    <script>
        function formValidator() {
            var Item_Nm = document.getElementById("txtItem_Nm");
            var Item_Rate = document.getElementById("txtItem_Rate");
            var Item_Stock = document.getElementById("txtItem_Stock");
            var Item_Descr = document.getElementById("txtItem_Descr");
            var Item_Photo = document.getElementById("txtItem_Photo");

            if (notEmpty(Item_Nm, "Item name required")) {
                if (notEmpty(Item_Rate, "Item rate required") && isNumeric(Item_Rate, "Rate must be numeric")) {
                    if (notEmpty(Item_Stock, "Stock required") && isNumeric(Item_Stock, "Stock must be numeric")) {
                        if (notEmpty(Item_Descr, "Description required")) {
                            if (notEmpty(Item_Photo, "Photo required")) {
                                return true;
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

<div class="container mt-5">

    <h2 class="page-title">Item Master Management</h2>

    <!-- FORM CARD -->
    <div class="card p-4 mb-5">
        <form method="POST" action="/itemmaster" enctype="multipart/form-data">

            <div class="row g-3">

                <div class="col-md-4">
                    <label class="form-label">Item ID</label>
                    <input type="text" class="form-control" name="Item_Id" value="{{ Item_Id }}">
                </div>

                <div class="col-md-4">
                    <label class="form-label">Item Name</label>
                    <input type="text" class="form-control" name="Item_Nm" id="txtItem_Nm" value="{{ Item_Nm }}">
                </div>

                <div class="col-md-4">
                    <label class="form-label">Company</label>
                   <select name="Comp_Id" class="form-select"
                        {% if role=='ShopOwner' %}disabled{% endif %}>
                    {% for c in comp_list %}
                    <option value="{{ c[0] }}"
                        {% if c[0]|string == Comp_Id|string %}selected{% endif %}>
                        {{ c[1] }}
                    </option>
                    {% endfor %}
                    </select>
                </div>

                <div class="col-md-4">
                    <label class="form-label">Category</label>
                    <select name="Cat_Id" class="form-select">
                        {% for c in cat_list %}
                        <option value="{{ c[0] }}" {% if c[0]|string == Cat_Id|string %}selected{% endif %}>
                            {{ c[1] }}
                        </option>
                        {% endfor %}
                    </select>
                </div>

                <div class="col-md-4">
                    <label class="form-label">Brand</label>
                    <select name="Brand_Id" class="form-select">
                        {% for b in brand_list %}
                        <option value="{{ b[0] }}" {% if b[0]|string == Brand_Id|string %}selected{% endif %}>
                            {{ b[1] }}
                        </option>
                        {% endfor %}
                    </select>
                </div>

                <div class="col-md-4">
                    <label class="form-label">Item Rate</label>
                    <input type="text" class="form-control" name="Item_Rate" id="txtItem_Rate" value="{{ Item_Rate }}">
                </div>

                <div class="col-md-4">
                    <label class="form-label">Item Stock</label>
                    <input type="text" class="form-control" name="Item_Stock" id="txtItem_Stock" value="{{ Item_Stock }}">
                </div>

                <div class="col-md-4">
                    <label class="form-label">Description</label>
                    <input type="text" class="form-control" name="Item_Descr" id="txtItem_Descr" value="{{ Item_Descr }}">
                </div>

                <div class="col-md-4">
                    <label class="form-label">Item Photo</label>
                    <input type="file" class="form-control" name="Item_Photo" id="txtItem_Photo">
                </div>

            </div>

            <div class="mt-4">
                <input type="submit" value="Insert" name="btn"
                       onclick="return formValidator()"
                       class="btn btn-primary"
                       {% if is_record %}disabled{% endif %}>

                <input type="submit" value="Update" name="btn"
                       onclick="return formValidator()"
                       class="btn btn-success"
                       {% if not is_record %}disabled{% endif %}>

                <input type="submit" value="Delete" name="btn"
                       class="btn btn-danger"
                       {% if not is_record %}disabled{% endif %}>
            </div>

        </form>
    </div>

    <!-- TABLE CARD -->
    {% if Item_list %}
    <div class="card p-3">
        <table class="table table-hover align-middle">
            <thead>
            <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Company</th>
                <th>Category</th>
                <th>Brand</th>
                <th>Rate</th>
                <th>Stock</th>
                <th>Description</th>
                <th>Photo</th>
                <th>Action</th>
            </tr>
            </thead>
            <tbody>
            {% for row in Item_list %}
            <tr>
                <td>{{ row[0] }}</td>
                <td>{{ row[1] }}</td>
                <td>{{ row[2] }}</td>
                <td>{{ row[3] }}</td>
                <td>{{ row[4] }}</td>
                <td>{{ row[5] }}</td>
                <td>{{ row[6] }}</td>
                <td>{{ row[7] }}</td>
                <td>{{ row[8] }}</td>
                <td>
                    <a href="/itemmaster?Item_Id={{ row[0] }}&Item_Nm={{ row[1] }}&Comp_Id={{ row[2] }}&Cat_Id={{ row[3] }}&Brand_Id={{ row[4] }}&Item_Rate={{ row[5] }}&Item_Stock={{ row[6] }}&Item_Descr={{ row[7] }}&Item_Photo={{ row[8] }}"
                       class="btn btn-sm btn-outline-primary">
                        Select
                    </a>
                </td>
            </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}

</div>
</body>
</html>
"""


    return render_template_string(html_template,
                                   Item_list=Item_list,
                                   comp_list=comp_list,
                                   cat_list=cat_list,
                                   brand_list=brand_list,
                                   Item_Id=Item_Id,
                                   Item_Nm=Item_Nm,
                                   Comp_Id=Comp_Id,
                                   Cat_Id=Cat_Id,
                                   Brand_Id=Brand_Id,
                                   Item_Rate=Item_Rate,
                                   Item_Stock=Item_Stock,
                                   Item_Descr=Item_Descr,
                                   Item_Photo=Item_Photo,
                                   is_record=is_record,role=role)

