from .extensions import db
import datetime

class CProgramModel(db.Model):
    __tablename__ = 'c_program_model'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False) 
    repo_url = db.Column(db.String, unique=False, nullable=False)
    repo_branch = db.Column(db.String, unique=False, nullable=False)
    build_cmd = db.Column(db.String, nullable=False, default="make")
    build_dir = db.Column(db.String, nullable=False, default="./")
    latest_commit = db.Column(db.String(40), nullable=True) 

    
    # Define the relationship to ArtifactModel
    artifacts = db.relationship('ArtifactModel', backref='program', lazy=True)
    
    # Define the relationship to BuildStatusModel
    build_statuses = db.relationship('BuildStatusModel', backref='program', lazy=True)

    def __repr__(self):
        return f"CProgram(name={self.name}, repo_url={self.repo_url})"

class ArtifactModel(db.Model):
    __tablename__ = 'artifact_model'

    artifact_id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('c_program_model.id'), nullable=False)
    artifact_name = db.Column(db.String(80), nullable=False)
    artifact_path = db.Column(db.String, nullable=False)
    version = db.Column(db.String, nullable=False, default="1.0.0")
    artifact_data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f"Artifact(program_id={self.program_id}, artifact_path={self.artifact_path})"

class BuildStatusModel(db.Model):
    __tablename__ = 'build_status_model'

    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('c_program_model.id'), nullable=False)
    checksum = db.Column(db.String(64), nullable=False)  # Updated to store the checksum
    status = db.Column(db.String(20), nullable=False)  # Status can be 'completed', 'failed', 'building'
    timestamp = db.Column(db.DateTime, nullable=False, default=lambda: datetime.datetime.now(datetime.timezone.utc))
    log = db.Column(db.Text, nullable=True)  # Store build logs or error messages

    def __repr__(self):
        return f"BuildStatus(program_id={self.program_id}, checksum={self.checksum}, status={self.status})"
