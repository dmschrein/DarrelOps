"""Defines APIs for registering C programs"""

from flask import jsonify, request
from flask_restful import Resource, reqparse, fields, marshal_with
import os
from ..extensions import db
from werkzeug.utils import secure_filename
from ..models import CProgramModel
from sqlalchemy.exc import IntegrityError
from ..services.build_service import build_program
from ..services.deploy_service import deploy_artifact
from ..services.package_service import package_artifact
from ..services.util import allowed_file

import logging


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

class RegisterProgram(Resource):
    @marshal_with(programFields)
    def post(self):
        logger = logging.getLogger('RegisterProgram')
        
        logger.info("Received request to register a new program.")
        
        try:
            """ASSUMPTION: User would register the project with a git repository
            TODO: handle in future versions if user wants this option.
            """
            if 'files' in request.files:
                uploaded_file = request.files['files']
                if uploaded_file.filename == '':
                    logger.warning("No selected file in the request.")
                    return jsonify({'error': 'No selected file'}), 400
                 
                if allowed_file(uploaded_file.filename):
                    filename = secure_filename(uploaded_file.filename)
                    destination = os.path.join('uploads/', filename)
                    uploaded_file.save(destination)
                    logger.info(f"File uploaded and saved at {destination}.")
                
                    program = CProgramModel(
                        name=filename.rsplit('.', 1)[0],
                        repo_url=None,
                        repo_branch=None,
                        build_cmd="make",
                        build_dir="./"
                    )
                else:
                    logger.error("Invalid file type.")
                    return jsonify({'error': 'Invalid file type'}), 400
                 
            elif 'repo_url' in request.json:
                repo_url = request.json['repo_url']
                name = request.json.get('name', repo_url.split('/')[-1].replace('.git', ''))
                repo_branch = request.json['repo_branch']
                build_cmd = request.json.get('build_cmd', 'make')
                build_dir = request.json.get('build_dir', './')

                program = CProgramModel(
                    name=name,
                    repo_url=repo_url,
                    repo_branch=repo_branch,
                    build_cmd=build_cmd,
                    build_dir=build_dir
                )
                        
            else:
                logger.error("No file or repo URL provided.")
                return jsonify({'error': 'No file or repo URL provided'}), 400
            
            if program:
                # Save the program to the database before triggering the build
                try:
                    db.session.add(program)
                    db.session.commit()
                    logger.info(f"Program {program.name} saved successfully with ID {program.id}.")
                except IntegrityError as e:
                    db.session.rollback()
                    logger.error(f"IntegrityError: {str(e.orig)}")
                    return jsonify({'error': 'Program with this name already exists. Please choose a different name.'}), 400

                # Now trigger the build, since program.id is now set
                logger.info(f"Starting build for program {program.name}.")
                build_success = build_program(program)
                
                if build_success:
                    logger.info(f"Build succeeded for program {program.name}. Packaging artifact.")
                    
                    artifact_path, new_version = package_artifact(program)
                    if artifact_path:
                        logger.info(f"Artifact successfully packaged for program {program.name}. Starting deployment.")
                        deploy_success = deploy_artifact(artifact_path, program, version=new_version)
                    
                        if deploy_success:
                            logger.info(f"Deployment succeeded for version {new_version} for program {program.name}.")
                            return program, 201
                        else:
                            logger.error(f"Deployment failed for program {program.name}")
                            return jsonify({'error': 'Program registered and built, but deployment failed'}), 500
                            
                    else:
                        logger.error(f"Packaging artifact failed for program {program.name}")
                        return jsonify({'error': 'Program registered and built, but packaging artifact failed'}), 500
                else:
                    logger.error(f"Build failed for program {program.name}.")
                    return jsonify({'error': 'Program registered, but build failed'}), 500

        except Exception as e:
            db.session.rollback()
            logger.error(f"An unexpected error occurred: {str(e)}")
            return jsonify({'error': 'An unexpected error occurred. Please try again later.'}), 500

        logger.error("Registration failed for unknown reasons.")  
        return jsonify({'error': 'Registration failed'}), 500
    
    @marshal_with(programFields)
    def get(self):
        programs = CProgramModel.query.all()
        return programs, 200
    