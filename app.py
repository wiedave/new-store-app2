from flask import Flask,render_template,redirect,url_for,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager,UserMixin,login_user,login_required,logout_user,current_user
from werkzeug.security import generate_password_hash,check_password_hash
from form import LoginForm,AdduserForm,EdituserForm,PasswordForm
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkeyyes'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://gunawan:Belajar2020@192.168.100.99/hadi_produk_list'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
Migrate(app,db)

####MODELS######
class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64),unique=True)
    password = db.Column(db.String(128))
    role = db.Column(db.String(64))

    def __init__(self,username,password,role):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def __repr__(self):
        return f"username:{self.username} role:{self.role}"


class Group(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    groupname = db.Column(db.String(64))

    products = db.relationship('Product',backref='grup',lazy=True)

    def __repr__(self):
        return f"groupname:{self.groupname}"


class Brand(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    brandname = db.Column(db.String(64))

    products = db.relationship('Product',backref='merek',lazy=True)

    def __repr__(self):
        return f"brandname:{self.brandname}"

class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(128))
    price = db.Column(db.Integer)
    photo = db.Column(db.String(128))

    group_id = db.Column(db.Integer,db.ForeignKey('group.id'))
    brand_id = db.Column(db.Integer,db.ForeignKey('brand.id'))

    def __repr__(self):
        return f"Nama Produk:{self.name} -- Harga:{self.price} --group_id:{self.group_id} --brand_id:{self.brand_id}"

###MODELS###########


login_manager = LoginManager(app)

login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/adm2')
@login_required
def admin():
    return render_template("admin.html")

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Log in Success')

            next = request.args.get('next')
            if next == None or not next[0] == '/adm2':
                next = url_for('admin')
                return redirect(next)
        else:
            flash("User not found or wrong Password!")
            return redirect(url_for('login'))
    return render_template('login.html',form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('you are logout now')
    return redirect(url_for('login'))

@app.route('/adm2/users')
@login_required
def users():
    users = User.query.all()

    return render_template('users.html', users=users)

@app.route('/adm2/addusers', methods=['GET','POST'])
@login_required
def addusers():
    users = User.query.all()
    form = AdduserForm()
    if form.validate_on_submit():
        cek = User.query.filter_by(username=form.username.data).first()

        if not cek :
            user = User(username=form.username.data,password=form.password.data,role=form.role.data)
            db.session.add(user)
            db.session.commit()
            flash('thank you User has registered')
            return redirect(url_for('users'))
        else:
            flash('Username already registered')
            return redirect(url_for('addusers'))
    return render_template('addusers.html', users=users, form=form)


@app.route('/adm2/edit/<int:user_id>', methods=['GET','POST'])
@login_required
def edit(user_id):
    users = User.query.filter_by(id=user_id).first()
    form = EdituserForm()

    if form.validate_on_submit():
        users.username = form.username.data
        users.role = form.role.data
        db.session.commit()
        flash('Users has been updated')
        return redirect(url_for('users'))

    elif request.method == 'GET':
        form.username.data = users.username
        form.role.data = users.role
    return render_template("editusers.html", users=users ,form=form)

@app.route('/adm2/password/<int:user_id>', methods=['GET','POST'])
@login_required
def password(user_id):
    users = User.query.filter_by(id=user_id).first()
    form = PasswordForm()

    if form.validate_on_submit():
        users.password = generate_password_hash(form.password.data)
        db.session.commit()
        flash('Password Changed')
        return redirect(url_for('users'))

    return render_template("passwordusers.html", form=form,users=users)

@app.route('/adm2/delete/<int:user_id>', methods=['GET','POST'])
@login_required
def delete_user(user_id):
    delete_user = User.query.filter_by(id=user_id).first()
    db.session.delete(delete_user)
    db.session.commit()
    flash('User has been deleted')
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True)
