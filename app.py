from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.secret_key = 'xnxx.com'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dealer_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    information = db.Column(db.Text, nullable=False)
    miscelleneous = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
user_credentials = {'user': '123'}
admin_credentials = {'admin': '123'}
@app.route('/')
def index():
    return render_template('login.html')
@app.route('/login', methods=['POST'])
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
@app.route('/home')
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect('/')
@app.route('/admin/home')
def admin_home():
    if 'admin' in session:
        user_data = User.query.all()
        return render_template('admin_home.html', user_data=user_data)
    else:
        return redirect('/')
@app.route('/submit', methods=['POST'])
def submit():
    if 'user' in session:
        dealer_name = request.form['dealer_name']
        amount = request.form['amount']
        information = request.form['information']
        miscelleneous = request.form['miscelleneous']
        date = request.form['date']
        new_user = User(dealer_name=dealer_name, amount=amount, information=information, miscelleneous=miscelleneous, date=date)
        db.session.add(new_user)
        db.session.commit()
    return redirect('/home')
@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('admin', None)
    return redirect('/')
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
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
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    user_data = User.query.get(id)
    db.session.delete(user_data)
    db.session.commit()
    # clovetech4@gmail.com
    return redirect('/admin/home')
# if __name__ == '__main__':
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)
