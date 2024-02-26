import os 
from flask import Flask
from .extensions import db
from .routes import main
# db = SQLAlchemy(app)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'abcd.com'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL") #'sqlite:///data.db'
    db.init_app(app)
    
    app.register_blueprint(main)
    
    return app
