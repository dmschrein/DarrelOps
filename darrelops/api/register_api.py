from flask import jsonify, request, abort
from flask_restful import Resource, reqparse, fields, marshal_with
import os
import logging
from sqlalchemy.exc import IntegrityError

from ..extensions import db
from werkzeug.utils import secure_filename
from ..models import CProgramModel
from ..services.build_service import build_program
from ..services.deploy_service import deploy_artifact
from ..services.package_service import package_artifact
from ..services.util import allowed_file


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
            program = self._initialize_program(request)
            if not program:
                abort(400, description='No file or repo URL provided.')
            
            self._save_program_to_db(program)

            logger.info(f"Starting build for program {program.name}.")
            build_success = build_program(program)
            
            if build_success:
                return self._handle_successful_build(program)
            else:
                logger.error(f"Build failed for program {program.name}.")
                abort(500, description='Program registered, but build failed')

        except IntegrityError as e:
            db.session.rollback()
            logger.error(f"IntegrityError: {str(e.orig)}")
            abort(400, description='Program with this name already exists. Please choose a different name.')
        except Exception as e:
            db.session.rollback()
            logger.error(f"An unexpected error occurred: {str(e)}")
            abort(500, description='An unexpected error occurred. Please try again later.')

    def _initialize_program(self, request):
        if 'files' in request.files:
            return self._handle_file_upload(request.files['files'])
        elif 'repo_url' in request.json:
            return self._handle_repo_registration(request.json)
        return None

    def _handle_file_upload(self, uploaded_file):
        logger = logging.getLogger('RegisterProgram')
        if uploaded_file.filename == '':
            logger.warning("No selected file in the request.")
            abort(400, description='No selected file')

        if allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            destination = self._save_uploaded_file(filename, uploaded_file)
            logger.info(f"File uploaded and saved at {destination}.")
            
            return CProgramModel(
                name=filename.rsplit('.', 1)[0],
                repo_url=None,
                build_cmd="make",
                build_dir="./"
            )
        else:
            logger.error("Invalid file type.")
            abort(400, description='Invalid file type')

    def _save_uploaded_file(self, filename, uploaded_file):
        upload_dir = 'uploads/'
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
        destination = os.path.join(upload_dir, filename)
        uploaded_file.save(destination)
        return destination

    def _handle_repo_registration(self, json_data):
        name = json_data.get('name', json_data['repo_url'].split('/')[-1].replace('.git', ''))
        build_cmd = json_data.get('build_cmd', 'make')
        build_dir = json_data.get('build_dir', './')
        
        return CProgramModel(
            name=name,
            repo_url=json_data['repo_url'],
            build_cmd=build_cmd,
            build_dir=build_dir
        )

    def _save_program_to_db(self, program):
        logger = logging.getLogger('RegisterProgram')
        db.session.add(program)
        db.session.commit()
        logger.info(f"Program {program.name} saved successfully with ID {program.id}.")

    def _handle_successful_build(self, program):
        logger = logging.getLogger('RegisterProgram')
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
                abort(500, description='Program registered and built, but deployment failed')
        else:
            logger.error(f"Packaging artifact failed for program {program.name}")
            abort(500, description='Program registered and built, but packaging artifact failed')

    @marshal_with(programFields)
    def get(self):
        programs = CProgramModel.query.all()
        return programs, 200
