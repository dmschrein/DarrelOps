import os
import shutil
import logging
from darrelops.models import ArtifactModel
from darrelops.utils.extensions import app, db

# deploy artifact to filesystem
# def deploy_to_artifactory(artifact: ArtifactModel):
#     logger = logging.getLogger('DeployService')
#     logger.info(f"Deploying artifact for program {artifact.version} for program ID {artifact.program_id} to Artifactory.")

#     #base_dir = os.getenv('ARTIFACTORY_BASE_DIR', os.path.abspath(os.path.dirname(__file__)))
#     deploy_dir = os.path.join(ARTIFACTORY_BASE_DIR, str(artifact.program_id), artifact.version)
#     os.makedirs(deploy_dir, exist_ok=True)

#     try:
#         shutil.move(artifact.artifact_path, deploy_dir)
#         logger.info(f"Artifact for {artifact.version} for program ID {artifact.program_id} deployed to {deploy_dir}.")
#         return True
#     except Exception as e:
#         logger.error(f"Deployment failed for program ID {artifact.program_id}: {str(e)}")
#         return False

# deploy to database       
def deploy_to_artifactory_db(program, artifact_path:str):
    logger = logging.getLogger('DeployService')
    logger.info(f"Deploying artifact for program {program['version']} for program ID to Artifactory database.")
    
    try:
        # read artifact
        with open(artifact_path, 'rb') as artifact_file:
            artifact_data = artifact_file.read()
            
        with app.app_context():
            artifact= ArtifactModel(
                program_id=program['id'],
                artifact_name=os.path.basename(artifact_path),
                artifact_version=program['version'],
                artifact_data=artifact_data
            )
            db.session.add(artifact)
            db.session.commit()
            logger.info(f"Artifact entry created in Artifactory database for program {program['name']}")

        return True
    except Exception as e:
        logger.error(f"Deployment failed for program ID {program['id']}: {str(e)}")
        return False