"""Models"""
# darrelops/models.py

from .extensions import db

class CProgramModel(db.Model):
    __bind_key__ = 'cprogram_db'
    __tablename__ = 'c_program_model'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False) # Explain 80
    repo_url = db.Column(db.String, unique=False, nullable=False)
    build_cmd = db.Column(db.String, nullable=False, default="make")
    build_dir = db.Column(db.String, nullable=False, default="./")
    version = db.Column(db.String, nullable=False, default="1.0.0")

    def __repr__(self):
        return f"CProgram(name = {self.name}, version = {self.version})"
    
class ArtifactModel(db.Model):
    __bind_key__ = 'artifact_db'
    __tablename__ = 'artifact_model'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('c_program_model.id'), nullable=False)
    artifact_name = db.Column(db.String, nullable=False)
    artifact_version = db.Column(db.String, nullable=False, default="1.0.0")
    artifact_data = db.Column(db.LargeBinary, nullable=False)
   
    def __repr__(self):
        return f"Artifact(program_id={self.program_id}, artifact_name={self.artifact_name})"