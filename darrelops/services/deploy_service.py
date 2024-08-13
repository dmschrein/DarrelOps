
# darrelops/serivces/deploy_service.py

import os
import logging
from darrelops.models import db, ArtifactModel, CProgramModel

def deploy_artifact(artifact_path, program: CProgramModel):
    logger = logging.getLogger('DeployService')
    logger.info(f"Deploying artifact for program {program.name} to the database.")

    try:
        # Reading the artifact as binary data
        with open(artifact_path, 'rb') as artifact_file:
            artifact_data = artifact_file.read()
        
        artifact_name = os.path.basename(artifact_path)

        # Creating an ArtifactModel entry
        artifact = ArtifactModel(
            program_id=program.id,
            artifact_name=artifact_name,
            artifact_path=artifact_path,
            artifact_data=artifact_data
        )

        # Adding the artifact to the database session and committing
        db.session.add(artifact)
        db.session.commit()

        logger.info(f"Artifact {artifact_name} for program {program.name} deployed to the database successfully.")
        return True
    except Exception as e:
        logger.error(f"Deployment to database failed for program {program.name}: {str(e)}")
        return False
