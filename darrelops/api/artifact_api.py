"""Artifact api to retrieve bundled artifacts"""

from flask_restful import Resource
from flask import send_file
from darrelops.models import ArtifactModel
from io import BytesIO

class DownloadArtifact(Resource):
    def get(self, program_id, version):
        artifact = ArtifactModel.query.filter_by(program_id=program_id, artifact_version=version).first()
        
        if not artifact:
            logger.error(f"Artifact not found for program ID {program_id} and version {version}.")
            abort(404, description="Artifact not found")

        # Create a file-like object from the binary data
        artifact_file = BytesIO(artifact.artifact_data)
        artifact_file.seek(0)

        # Send the file to the client
        return send_file(artifact_file, attachment_filename=artifact.artifact_name, as_attachment=True)

# Add the resource to the API
api.add_resource(DownloadArtifact, '/api/artifact/download/<int:program_id>/<string:version>')