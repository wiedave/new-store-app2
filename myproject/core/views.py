from flask import Blueprint,render_template
from myproject.models import Product

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

@core.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products, harga=harga)

@core.route('/learn_more')
def learn_more():
    return 'Hah go back to the nether to kill piglins!'#render_template("index.html")
