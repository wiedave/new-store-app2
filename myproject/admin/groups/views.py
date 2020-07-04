from flask import Blueprint,render_template,redirect,url_for,flash,request
from flask_login import login_required
from myproject import db
from myproject.models import Group
from myproject.admin.groups.forms import GroupForm

group_bp = Blueprint('groups',__name__,template_folder='templates/group')

@group_bp.route('/')
@login_required
def group():
    grup = Group.query.all()
    return render_template("groups.html",grouplist=grup)


@group_bp.route('/add', methods=['GET','POST'])
@login_required
def add():
    form = GroupForm()
    if form.validate_on_submit():
        cek = Group.query.filter_by(groupname=form.groupname.data).first()
        if not cek:
            grup = Group(groupname=form.groupname.data)
            db.session.add(grup)
            db.session.commit()
            flash("Product Group Added")
            return redirect(url_for('groups.group'))
        else:
            flash("Product Group Exist !!!")
            return redirect(url_for('groups.add'))

    return render_template("addgroups.html",form=form)

@group_bp.route('/edit/<int:group_id>', methods=['GET','POST'])
@login_required
def edit(group_id):
    grups = Group.query.filter_by(id=group_id).first()
    form = GroupForm()

    if form.validate_on_submit():
        cek = Group.query.filter_by(groupname=form.groupname.data).first()
        if not cek :
            grups.groupname = form.groupname.data
            db.session.commit()
            flash("Product Group has been Updated")
            return redirect(url_for('groups.group'))
        else:
            flash('Product Group not change or already exist!!!')
            return redirect(url_for('groups.edit',group_id=grups.id))

    elif request.method == 'GET':
        form.groupname.data = grups.groupname

    return render_template("editgroups.html",grup_select=grups, form=form)

@group_bp.route('/delete/<int:group_id>',methods=['GET','POST'])
@login_required
def delete(group_id):
    delete_grups = Group.query.filter_by(id=group_id).first()
    db.session.delete(delete_grups)
    db.session.commit()
    flash('Product Group has been deleted!!!')
    return redirect(url_for('groups.group'))
