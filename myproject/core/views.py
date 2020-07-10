from flask import Blueprint,render_template, request, redirect, url_for
from myproject.models import Product
from myproject.core.forms import SearchForm

core = Blueprint('core',__name__,template_folder='templates/core')

def harga(price):
    num = list(str(price))
    if len(num) == 4 or len(num) == 5 or len(num) == 6:
        num.insert(-3,'.')
    elif len(num) == 7 or len(num) == 8 or len(num) == 9:
        num.insert(-3,'.')
        num.insert(-7,'.')
    elif len(num) == 10 or len(num) == 11 or len(num) == 12:
        num.insert(-3,'.')
        num.insert(-7,'.')
        num.insert(-11,'.')
    num = "".join(num)
    return num

@core.route('/', methods=["GET", "POST"])
def index():
    products = Product.query.all()
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for('core.search', search=form.search.data))

    return render_template("index.html", products=products, harga=harga, form=form)

@core.route('/search/<search>', methods=["GET", "POST"])
def search(search):
    form = SearchForm()
    sea = str(search)
    product = Product.query.filter(Product.name.like('%'+sea+'%')).all()
    if form.validate_on_submit():
        return redirect(url_for('core.search', search=form.search.data))


    return render_template('search.html', search=product, harga=harga, name=sea, form=form)

@core.route('/learn_more/<int:id>')
def learn_more(id):
    product = Product.query.filter(Product.id==id).first()

    return render_template("read_more.html", product=product)
