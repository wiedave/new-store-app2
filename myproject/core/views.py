from flask import Blueprint,render_template
from myproject.models import Product

core = Blueprint('core',__name__,template_folder='templates/core')


@core.route('/')
def index():
    products = Product.query.all()
    return render_template("index.html", products=products)

@core.route('/learn_more')
def learn_more():
    return 'Hah go back to the nether to kill piglins!'#render_template("index.html")
