
# darrelops/services/package_service.py
import shutil
import os
from darrelops.models import CProgramModel, ArtifactModel

# packages build output into zip file
import shutil
import os
from darrelops.models import CProgramModel, ArtifactModel

def package_artifact(program: CProgramModel):
    # Determine the directory for storing the artifacts
    artifact_dir = os.path.join('artifacts', program.name, program.build_dir)
    os.makedirs(artifact_dir, exist_ok=True)

    # Determine the latest version of the artifact
    latest_artifact = ArtifactModel.query.filter_by(program_id=program.id).order_by(ArtifactModel.artifact_id.desc()).first()
    
    if latest_artifact:
        # Parse the latest version to determine the next version
        version_parts = latest_artifact.version.split('.')
        
        # Assuming the version is in the form of 1.0.RC1 or 1.0.RELEASE
        if "RC" in version_parts[-1]:
            rc_version = int(version_parts[-1].replace("RC", "")) + 1
            new_version = f"{version_parts[0]}.{version_parts[1]}.RC{rc_version}"
        elif version_parts[-1] == "RELEASE":
            new_version = f"{version_parts[0]}.{version_parts[1]}.RELEASE"
        else:
            # If it's a final version without RC, increment the patch number
            new_version = f"{version_parts[0]}.{version_parts[1]}.RC1"
    else:
        # Default to version 1.0.0.RC1 if no previous version exists
        new_version = "1.0.RC1"

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
