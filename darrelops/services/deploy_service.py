import os
import shutil
import logging
from darrelops.models import CProgramModel

def deploy_to_artifactory(artifact_path, program: CProgramModel):
    logger = logging.getLogger('DeployService')
    logger.info(f"Deploying artifact for program {program.name} to Artifactory.")

    deploy_dir = os.path.join('artifactory', program.name)
    os.makedirs(deploy_dir, exist_ok=True)

    try:
        shutil.move(artifact_path, deploy_dir)
        logger.info(f"Artifact for {program.name} deployed to {deploy_dir}.")
        return True
    except Exception as e:
        logger.error(f"Deployment failed for program {program.name}: {str(e)}")
        return False
