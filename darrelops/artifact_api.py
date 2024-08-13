# from flask_restful import Resource, fields, marshal_with
# from flask import send_file, abort, request
# from .extensions import api
# from darrelops.models import ArtifactModel
# from io import BytesIO
# import logging

# # Define the output format for the artifacts
# artifact_fields = {
#     'artifact_id': fields.Integer,
#     'program_id': fields.Integer,
#     'artifact_name': fields.String,
#     'artifact_path': fields.String,
#     'version': fields.String,
# }

# class ListArtifacts(Resource):
#     @marshal_with(artifact_fields)
#     def get(self, program_id=None):
#         logger = logging.getLogger('ListArtifacts')

#         if program_id:
#             # Query all artifacts associated with the given program_id
#             artifacts = ArtifactModel.query.filter_by(program_id=program_id).all()
#             if not artifacts:
#                 logger.info(f"No artifacts found for program ID {program_id}.")
#                 return {'message': 'No artifacts found for this program.'}, 404
#             logger.info(f"Found {len(artifacts)} artifacts for program ID {program_id}.")
#         else:
#             # Query all artifacts in the database
#             artifacts = ArtifactModel.query.all()
#             logger.info(f"Found {len(artifacts)} artifacts in total.")

#         return artifacts, 200

# class DownloadArtifact(Resource):
#     def get(self, program_id, version):
#         logger = logging.getLogger('DownloadArtifact')

#         # Query the artifact based on program_id and version
#         artifact = ArtifactModel.query.filter_by(program_id=program_id, version=version).first()
        
#         if not artifact:
#             logger.error(f"Artifact not found for program ID {program_id} and version {version}.")
#             abort(404, description="Artifact not found")

#         # Create a file-like object from the binary data
#         artifact_file = BytesIO(artifact.artifact_data)
#         artifact_file.seek(0)

#         # Send the file to the client with the correct filename
#         return send_file(
#             artifact_file, 
#             download_name=artifact.artifact_name, 
#             as_attachment=True
#         )

# # Add the resources to the API
# api.add_resource(DownloadArtifact, '/api/artifact/download/<int:program_id>/<string:version>')
# api.add_resource(ListArtifacts, '/api/artifacts', '/api/artifacts/<int:program_id>')
