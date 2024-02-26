from flask import Blueprint, redirect, url_for, Flask, render_template, request, session
from .extensions import db
from .models import User

main = Blueprint('main', __name__)

user_credentials = {'user': '123'}
admin_credentials = {'admin': '123'}


@main.route('/')
def index():
    return render_template('login.html')


@main.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in user_credentials and user_credentials[username] == password:
        session['user'] = username
        return redirect('/home')
    elif username in admin_credentials and admin_credentials[username] == password:
        session['admin'] = username
        return redirect('/admin/home')
    else:
        return 'Invalid username or password'


@main.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect('/')


@main.route('/admin/home')
def admin_home():
    if 'admin' in session:
        user_data = User.query.all()
        return render_template('admin_home.html', user_data=user_data)
    else:
        return redirect('/')


@main.route('/submit', methods=['POST'])
def submit():
    if 'user' in session:
        dealer_name = request.form['dealer_name']
        amount = request.form['amount']
        information = request.form['information']
        miscelleneous = request.form['miscelleneous']
        date = request.form['date']
        new_user = User(dealer_name=dealer_name, amount=amount,
                        information=information, miscelleneous=miscelleneous, date=date)
        db.session.add(new_user)
        db.session.commit()
    return redirect('/home')


@main.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    return redirect('/')


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if request.method == 'GET':
        user_data = User.query.get(id)
        return render_template('edit.html', user_data=user_data)
    elif request.method == 'POST':
        user_data = User.query.get(id)
        user_data.dealer_name = request.form['dealer_name']
        user_data.amount = request.form['amount']
        user_data.information = request.form['information']
        user_data.miscelleneous = request.form['miscelleneous']
        user_data.date = request.form['date']
        db.session.commit()
        return redirect('/admin/home')


@main.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user_data = User.query.get(id)
    db.session.delete(user_data)
    db.session.commit()
    return redirect('/admin/home')
