from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# model
class CProgramModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) # Explain 80
    repo_url = db.Column(db.String, unique=True, nullable=False)
    build_cmd = db.Column(db.String, unique=True, nullable=False)
    build_dir = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return f"CProgram(name = {self.name}, repo_url = {self.repo_url})"
             
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help="File name cannot be blank")


@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)