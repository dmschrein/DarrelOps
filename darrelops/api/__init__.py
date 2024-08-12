"""Initialize the API and routes"""
# darrelops/api/__init__.py

from .artifact_api import DownloadArtifact
from .c_program_api import RegisterProgram
from ..utils.extensions import api

def initialize_routes(api, app):
    """Initialize all API routes."""
    # Register the API resources
    api.add_resource(DownloadArtifact, '/api/artifact/download/<int:program_id>/<string:version>')
    api.add_resource(RegisterProgram, '/api/register')

    # Add home route
    @app.route('/')
    def home():
        return '<h1>Flask REST API</h1>'