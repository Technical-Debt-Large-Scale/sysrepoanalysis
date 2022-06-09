from msr import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from msr.dao import Repository, User
from msr.forms import RegisterForm, LoginForm
from msr.main import usersCollection
import logging

# Remove all handlers associated with the root logger object.
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    datefmt='%d/%m/%Y %H:%M:%S', filename='logs/my_app_authentication.log', filemode='w')

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('authenticate/home.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email_address=form.email_address.data, password=form.password1.data)
        usersCollection.insert_user(user_to_create)
        login_user(user_to_create)
        msg = f"Account created successfully! You are now logged in as {user_to_create.username}"
        logging.info(msg)
        flash(msg, category='success')
        return redirect(url_for('msr_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('authenticate/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            msg = f'Success! You are logged in as: {attempted_user.username}'
            logging.info(msg)
            flash(msg, category='success')
            return redirect(url_for('msr_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('authenticate/login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    msg = "You have been logged out!"
    flash(msg, category='info')
    return redirect(url_for("home_page"))