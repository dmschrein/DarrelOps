"""Models"""
# darrelops/models.py

from .extensions import db

class CProgramModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) 
    repo_url = db.Column(db.String, unique=False, nullable=False)
    build_cmd = db.Column(db.String, nullable=False, default="make")
    build_dir = db.Column(db.String, nullable=False, default="./")

    def __repr__(self):
        return f"CProgram(name = {self.name}, repo_url = {self.repo_url})"
    
class ArtifactModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('c_program_model.id'), nullable=False)
    artifact_name = db.Column(db.String(80), unique=False, nullable=False)
    artifact_path = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False, default="1.0.0")
    artifact_data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f"Artifact(program_id={self.program_id}, artifact_path={self.artifact_path})"