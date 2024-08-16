"""Package Service"""

# darrelops/services/package_service.py
import shutil
import os
from darrelops.models import CProgramModel, ArtifactModel

# packages build output into zip file
import shutil
import os
from darrelops.models import CProgramModel, ArtifactModel

def package_artifact(program: CProgramModel):
    
    # sanitize repo url
    program_repo = str(program.repo_url)
    sanitized_url = program_repo.replace('https://', '').replace('/', '_')
    
    # Determine the directory for storing the artifacts
    artifactory_dir = 'artifactory'
    if not os.path.exists(artifactory_dir):
        os.makedirs(artifactory_dir)
    artifact_dir = os.path.join(artifactory_dir, 'artifacts', sanitized_url, program.repo_branch)
    os.makedirs(artifact_dir, exist_ok=True)

    # Determine the latest version of the artifact
    latest_artifact = ArtifactModel.query.filter_by(program_id=program.id).order_by(ArtifactModel.artifact_id.desc()).first()
    
    if latest_artifact:
        # Parse the latest version to determine the next version
        version_parts = list(map(int, latest_artifact.version.split('.')))
        version_parts[-1] += 1  # Increment the patch version
        new_version = '.'.join(map(str, version_parts))
    else:
        # Default to version 1.0.0 if no previous version exists
        new_version = "1.0.0"

    # Create the artifact name and path using the new version
    artifact_name = f"{program.name}-{new_version}.zip"
    artifact_path = os.path.join(artifact_dir, artifact_name)

    # Package the build output into a zip file
    shutil.make_archive(
        base_name=artifact_path.replace('.zip', ''), 
        format='zip', 
        root_dir=program.build_dir
    )
    
    # Return the path and new version of the artifact
    return artifact_path, new_version
