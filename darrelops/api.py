from flask import jsonify, request
from flask_restful import Resource, reqparse, fields, marshal_with
import os
import requests
from .extensions import app, db, api
from werkzeug.utils import secure_filename
from .models import CProgramModel
from .services.build_service import build_program
from .services.deploy_service import deploy_to_artifactory
from .services.util import allowed_file
import logging
import json

# json config
PROGRAMS_JSON_PATH = "registered_programs.json"

reg_program_args = reqparse.RequestParser()
reg_program_args.add_argument('name', type=str, required=True, help="Program name is required")
reg_program_args.add_argument('repo_url', type=str, required=True, help="Repository URL is required")
reg_program_args.add_argument('build_cmd', type=str, required=False, help="Build command")
reg_program_args.add_argument('build_dir', type=str, required=False, help="Build directory")


programFields = {
    'id': fields.Integer,
    'name': fields.String,
    'repo_url': fields.String,
    'build_cmd': fields.String,
    'build_dir': fields.String,
}

def load_programs():
    """Load registered programs from JSON file."""
    if os.path.exists(PROGRAMS_JSON_PATH):
        with open(PROGRAMS_JSON_PATH, 'r') as file:
            return json.load(file)
    return []

def save_programs(programs):
    """Save registered programs to JSON file."""
    with open(PROGRAMS_JSON_PATH, 'w') as file:
        json.dump(programs, file, indent=4)


def generate_program_id(programs):
    """Generate a new unique ID for the program."""
    if not programs:
        return 1
    max_id = max(program.get('id', 0) for program in programs)
    return max_id + 1

class RegisterProgram(Resource):
    @marshal_with(programFields)
    def post(self):
        logger = logging.getLogger('RegisterProgram')
        
        logger.info("Received request to register a new program.")
        
        programs = load_programs()
        program_id = generate_program_id(programs)
        
        if 'files' in request.files:
            uploaded_file = request.files['files']
            if uploaded_file.filename == '':
                logger.warning("No selected file in the request.")
                return jsonify({'error': 'No selected file'}), 400
             
            if allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                destination = os.path.join('uploads/', filename)
                uploaded_file.save(destination)
                logger.info(f"File uploaded and saved at {destination}.") # file registered
            
                program = {
                    "id": program_id,
                    "name": filename.rsplit('.', 1)[0],
                    "repo_url": None,
                    "build_cmd": "make",
                    "build_dir": "./"
                }
                program.append(program)
                save_programs(programs)
                logger.info(f"Program {program['name']} registered successfully.")
            else:
                logger.error("Invalid file type.")
                return jsonify({'error': 'Invalid file type'}), 400
             
        elif 'repo_url' in request.json:
            repo_url = request.json['repo_url']
            name = request.json.get('name', repo_url.split('/')[-1].replace('.git', ''))
            build_cmd = request.json.get('build_cmd', 'make')
            build_dir = request.json.get('build_dir', './')

            program = {
                "id": program_id,
                "name": name,
                "repo_url": repo_url,
                "build_cmd": build_cmd,
                "build_dir": build_dir
            }
                
            programs.append(program)
            save_programs(programs)
            logger.info(f"Program {program['name']} registered successfully from repository {repo_url}")
            
        else:
            logger.error("No file or repo URL provided.")
            return jsonify({'error': 'No file or repo URL provided'}), 400
        
        if program:
            logger.info(f"Starting build for program {program['name']}.")
            build_success = build_program(program)
            if build_success:
                logger.info(f"Build succeeded for program {program['name']}. Starting deployment.")
                deploy_success = deploy_to_artifactory(os.path.join(program['build_dir'], program['name']), program)
                if deploy_success:
                    logger.info(f"Deployment succeeded for program {program['name']}.")
                    return 201
                    
                else:
                    logger.error(f"Deployment failed for program {program['name']}")
                    return jsonify({'error': 'Program registered and built, but deployment failed'}), 500
            else:
                logger.error(f"Build failed for program {program['name']}.")
                return jsonify({'error': 'Program registered, but build failed'}), 500

        logger.error("Registration failed for unknown reasons.")  
        return jsonify({'error': 'Registration failed'}), 500
    
    @marshal_with(programFields)
    def get(self):
        programs = load_programs()
        return programs, 200
        
api.add_resource(RegisterProgram, '/api/register') 

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'   