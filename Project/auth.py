from flask import Blueprint,render_template,redirect,url_for,request,flash,session
from . import db
from .models import User
from flask_login import login_user, logout_user ,login_required,current_user
import re, os
from werkzeug.utils import secure_filename

auth = Blueprint("authentication",__name__)

UPLOAD_FOLDER = 'Project/static'
ALLOWED_EXTENSIONS = {'pdf'}


@auth.route("/signup", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get("name")
        username = request.form.get("username")
        pwd = request.form.get('pwd')
        pwdConfirm = request.form.get("confpwd")
        add = request.form.get('address')
        role = request.form.get('role')
        expy = request.form.get('expy')
        service_category = request.form.get('service-category')
        

        username_exists = User.query.filter_by(username=username).first()
                    
        if username_exists:
            flash('This username has already been chosen, please choose another one.', category='error')
        elif pwd != pwdConfirm:
            flash('Please type the same passwords', category='error')
        elif len(pwd) < 4:
            flash('Please choose a longer password.', category='error')
        else:
            newUser = User(name=name, username=username, password=pwd, address=add, role=role, pdf_filename=is_pdf_req(role), expy=expy, service=service_category)  # Set service category
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash("User Created", category='success')
            return redirect(url_for('authentication.login'))  # Redirect to login after signup
    return render_template("signup.html", user=current_user)


# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def is_pdf_req(role):
    if role == '1':
            pdf = request.files['pdf']

            if 'pdf' in request.files:
                file = request.files['pdf']
                if file.filename == '':
                    flash('No selected file.', category='error')
                    return redirect(url_for('authentication.sign_up'))
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    pdf_filename = filename
                else:
                    flash('Invalid file type. Only PDF files are allowed.', category='error')
                    return redirect(url_for('authentication.sign_up'))
    else:
        pdf_filename = None


@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('pwd')

        user = User.query.filter_by(username=username).first()

        if user:
            if (user.password == password):
                if user.role == 1:
                    flash("Logged in!",category='success')
                    login_user(user,remember=True)
                    return redirect(url_for('main.professional_home'))
                if user.role == 2:
                    flash("Logged in!",category='success')
                    login_user(user,remember=True)
                    return redirect(url_for('main.user_home'))
            else:
                flash('Password is incorrect',category='error')
        else:
            flash('Username does not exist',category='error')
    return render_template("login.html",user=current_user)

@auth.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        username = request.form.get('username')
        password = request.form.get('pwd')

        user = User.query.filter_by(username=username).first()

        if user:
            if (user.password == password):
                if user.role == 0:
                    flash("Logged in!",category='success')
                    login_user(user,remember=True)
                    return redirect(url_for('main.admin_home'))
            else:
                flash('Password is incorrect',category='error')
        else:
            flash('Username does not exist',category='error')
            return redirect(url_for('authentication.sign_up'))
    return render_template("admin_login.html",user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")