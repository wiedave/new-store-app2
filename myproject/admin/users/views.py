from flask import render_template,flash,request,redirect,url_for,Blueprint
from werkzeug.security import generate_password_hash
from flask_login import login_required,current_user,login_user,logout_user
from myproject import db
from myproject.models import User
from myproject.admin.users.forms import AdduserForm,EdituserForm,PasswordForm


users_bp = Blueprint('users',__name__,template_folder='templates/users')


@users_bp.route('/')
@login_required
def user():
    if current_user.role =="admin":
        page = request.args.get('page',1,type=int)
        users_list = User.query.order_by(User.id.desc()).paginate(page=page,per_page=5)
        return render_template('users.html', users_list=users_list)
    else:
        flash('You are not authorize!!!')
        return render_template('admin.html')

@users_bp.route('/add', methods=['GET','POST'])
@login_required
def add():
    if current_user.role == 'admin':
        users = User.query.all()
        form = AdduserForm()
        if form.validate_on_submit():
            cek = User.query.filter_by(username=form.username.data).first()

            if not cek :
                user = User(username=form.username.data,password=form.password.data,role=form.role.data)
                db.session.add(user)
                db.session.commit()
                flash('thank you User has registered')
                return redirect(url_for('users.users'))
            else:
                flash('Username already registered')
                return redirect(url_for('users.add'))
        return render_template('addusers.html', users=users, form=form)

    else:
        flash("You are not authorize !!!")
        return render_template("admin.html")

@users_bp.route('/edit/<int:user_id>', methods=['GET','POST'])
@login_required
def edit(user_id):
    if current_user.role == 'admin':
        users = User.query.filter_by(id=user_id).first()
        form = EdituserForm()

        if form.validate_on_submit():
            users.username = form.username.data
            users.role = form.role.data
            db.session.commit()
            flash('Users has been updated')
            return redirect(url_for('users.users'))

        elif request.method == 'GET':
            form.username.data = users.username
            form.role.data = users.role
        return render_template("editusers.html", users=users ,form=form)
    else:
        flash("You are not authorize!!!")
        return render_template("admin.html")

@users_bp.route('/password/<int:user_id>', methods=['GET','POST'])
@login_required
def password(user_id):
    if current_user.role == 'admin':
        users = User.query.filter_by(id=user_id).first()
        form = PasswordForm()

        if form.validate_on_submit():
            users.password = generate_password_hash(form.password.data)
            db.session.commit()
            flash('Password Changed')
            return redirect(url_for('users.users'))

        return render_template("passwordusers.html", form=form,users=users)
    else:
        flash("You are not authorize!!!")
        return render_template("admin.html")

@users_bp.route('/delete/<int:user_id>', methods=['GET','POST'])
@login_required
def delete(user_id):
    if current_user.role == 'admin':

        delete_user = User.query.filter_by(id=user_id).first()
        db.session.delete(delete_user)
        db.session.commit()
        flash('User has been deleted')
        return redirect(url_for('users.users'))
    else:
        flash("You are not authorize!!!")
        return render_template("admin.html")
