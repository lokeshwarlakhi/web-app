from .extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dealer_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    information = db.Column(db.Text, nullable=False)
    miscelleneous = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
