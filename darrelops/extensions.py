from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

# Initialize 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)
