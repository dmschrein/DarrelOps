from flask import jsonify, request, send_file, abort
from flask_restful import Resource, reqparse, fields, marshal_with
import os
import requests
from .extensions import app, db, api
from werkzeug.utils import secure_filename
from .models import CProgramModel, ArtifactModel
from .services.build_service import build_program
from .services.deploy_service import deploy_artifact
from .services.package_service import package_artifact
from .services.util import allowed_file



from io import BytesIO
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
        #program = None  # Initialize the program variable
        
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
                    build_cmd="make",
                    build_dir="./"
                )
                db.session.add(program)
                db.session.commit()
                logger.info(f"Program {program.name} registered successfully.")
            else:
                logger.error("Invalid file type.")
                return jsonify({'error': 'Invalid file type'}), 400
             
        elif 'repo_url' in request.json:
            repo_url = request.json['repo_url']
            name = request.json.get('name', repo_url.split('/')[-1].replace('.git', ''))
            build_cmd = request.json.get('build_cmd', 'make')
            build_dir = request.json.get('build_dir', './')

            program = CProgramModel(
                name=name,
                repo_url=repo_url,
                build_cmd=build_cmd,
                build_dir=build_dir
            )
                    
        else:
            logger.error("No file or repo URL provided.")
            return jsonify({'error': 'No file or repo URL provided'}), 400
        
        if program:
            logger.info(f"Starting build for program {program.name}.")
            build_success = build_program(program)
            if build_success:
                # store program
                db.session.add(program)
                db.session.commit()
                
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
                    logger.error(f"Deployment failed for program {program.name}")
                    return jsonify({'error': 'Program registered and built, but packaging artifact failed'}), 500
            else:
                logger.error(f"Build failed for program {program.name}.")
                return jsonify({'error': 'Program registered, but build failed'}), 500

        logger.error("Registration failed for unknown reasons.")  
        return jsonify({'error': 'Registration failed'}), 500
    
    @marshal_with(programFields)
    def get(self):
        programs = CProgramModel.query.all()
        return programs, 200
    
# Define the output format for the artifacts
artifact_fields = {
    'artifact_id': fields.Integer,
    'program_id': fields.Integer,
    'artifact_name': fields.String,
    'artifact_path': fields.String,
    'version': fields.String,
}

class ListArtifacts(Resource):
    @marshal_with(artifact_fields)
    def get(self, program_id=None):
        logger = logging.getLogger('ListArtifacts')

        if program_id:
            # Query all artifacts associated with the given program_id
            artifacts = ArtifactModel.query.filter_by(program_id=program_id).all()
            if not artifacts:
                logger.info(f"No artifacts found for program ID {program_id}.")
                return {'message': 'No artifacts found for this program.'}, 404
            logger.info(f"Found {len(artifacts)} artifacts for program ID {program_id}.")
        else:
            # Query all artifacts in the database
            artifacts = ArtifactModel.query.all()
            logger.info(f"Found {len(artifacts)} artifacts in total.")

        return artifacts, 200

class DownloadArtifact(Resource):
    def get(self, program_id, version):
        logger = logging.getLogger('DownloadArtifact')

        # Query the artifact based on program_id and version
        artifact = ArtifactModel.query.filter_by(program_id=program_id, version=version).first()
        
        if not artifact:
            logger.error(f"Artifact not found for program ID {program_id} and version {version}.")
            abort(404, description="Artifact not found")

        # Create a file-like object from the binary data
        artifact_file = BytesIO(artifact.artifact_data)
        artifact_file.seek(0)

        # Send the file to the client with the correct filename
        return send_file(
            artifact_file, 
            download_name=artifact.artifact_name, 
            as_attachment=True
        )
        
api.add_resource(RegisterProgram, '/api/register') 

api.add_resource(DownloadArtifact, '/api/artifact/download/<int:program_id>/<string:version>')
api.add_resource(ListArtifacts, '/api/artifacts', '/api/artifacts/<int:program_id>')

@app.route('/')
def home():
    return '<h1>Flask REST API</h1>'       
