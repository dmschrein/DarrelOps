"""Handles packaging the build output to ZIP file"""

import shutil
import os

# package the artifact for bundling
def package_artifact(program):
    artifact_dir = os.path.join('artifacts', program['name'], program['build_dir'])
    os.makedirs(artifact_dir, exist_ok=True)

    artifact_name = f"{program['name']}.zip"
    artifact_path = os.path.join(artifact_dir, artifact_name)

    shutil.make_archive(
        base_name=artifact_path.replace('.zip', ''), 
        format='zip', 
        root_dir=program['build_dir']
    )
    
    return artifact_path