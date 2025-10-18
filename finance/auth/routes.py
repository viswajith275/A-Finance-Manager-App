from flask import Blueprint,render_template,redirect,url_for,flash
from flask_bcrypt import generate_password_hash,check_password_hash
from .forms import LoginForm,RegisterForm
from flask_login import login_user,login_required,logout_user
from finance.models import User
from finance.extensions import db,login_manager

authbp = Blueprint('auth',__name__,template_folder='templates')


#for telling flask_login how to load users from db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@authbp.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existusr = User.query.filter_by(username=form.username.data).first()

        if existusr:
            flash('User already exist!')
            return redirect(url_for('auth.register'))


        hashpass = generate_password_hash(form.password.data)

        user = User(
                username=form.username.data,
                email=form.email.data,
                password=hashpass,

            )
        db.session.add(user)
        db.session.commit()
        flash('Account created Successfully now please login')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@authbp.route('/',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and check_password_hash(user.password,form.password.data):
            login_user(user)
            flash('Logged successfully!!')
            next_page = '/dashboard'  #now dont know
            return redirect(next_page)

        elif user:
            flash('Incorrect password!!')

        else:
            flash('Sign up first to login!!')
    return render_template('auth/login.html',form=form)

@authbp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged out successfully!')
    return redirect(url_for('auth.login'))
