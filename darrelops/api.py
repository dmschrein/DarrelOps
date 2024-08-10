from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# model
class CProgramModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) # Explain 80
    file_path = db.Column(db.String, unique=False, nullable=False)
    repo_url = db.Column(db.String, unique=True, nullable="N/A")
    build_cmd = db.Column(db.String, unique=True, nullable="make")
    build_dir = db.Column(db.String, unique=True, nullable="/")

    def __repr__(self):
        return f"CProgram(name = {self.name}, file_path = {self.file_path})"
          
program_args = reqparse.RequestParser()
program_args.add_argument('name', type=str, required=True, help="Name cannot be blank")
program_args.add_argument('file_path', type=str, required=True, help="File path name cannot be blank")

programFields = {
    'id':fields.Integer,
    'name':fields.String,
    'file_path':fields.String,
}

class CPrograms(Resource):
    @marshal_with(programFields)
    def get(self):
        cprograms = CProgramModel.query.all()
        return cprograms
    
    @marshal_with(programFields)
    def post(self):
        args = program_args.parse_args()
        program = CProgramModel(name=args["name"], file_path=args["file_path"])
        db.session.add(program)
        db.session.commit()
        programs = CProgramModel.query.all()
        return programs, 201


api.add_resource(CPrograms, '/api/cprograms/')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'

if __name__ == '__main__':
    app.run(debug=True)