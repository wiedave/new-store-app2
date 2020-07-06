from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_required
from myproject import db
from myproject.models import Product,Group,Brand
from myproject.admin.products.forms import ProductForm
from myproject.admin.products.picture_handler import add_product_pic

product_bp = Blueprint('products',__name__,template_folder='templates/product')


@product_bp.route('/')
@login_required
def product():
    list_product = Product.query.all()
    return render_template("products.html",list_product=list_product)

@product_bp.route('/add', methods=['GET','POST'])
@login_required
def add():
    form = ProductForm()
    if form.validate_on_submit():
        cek = Product.query.filter_by(name=form.name.data).first()
        if not cek :
            product_photo = add_product_pic(form.photo.data, form.name.data)
            product = Product(name=form.name.data,price=form.price.data,photo=product_photo,group_id=form.group.data.id,brand_id=form.brand.data.id)
            db.session.add(product)
            db.session.commit()
            flash("Product Added")
            return redirect(url_for('products.product'))
        else:
            flash("Product Name Exist !!!")
            return redirect(url_for('products.add'))

    return render_template("addproducts.html",form=form)
