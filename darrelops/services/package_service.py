import shutil
import os
from darrelops.models import CProgramModel

def package_artifact(program: CProgramModel):
    artifact_dir = os.path.join('artifacts', program.name, program.build_dir)
    os.makedirs(artifact_dir, exist_ok=True)

    artifact_name = f"{program.name}.zip"
    artifact_path = os.path.join(artifact_dir, artifact_name)

    shutil.make_archive(
        base_name=artifact_path.replace('.zip', ''), 
        format='zip', 
        root_dir=program.build_dir
    )
    
    return artifact_path
