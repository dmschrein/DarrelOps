"""Service to build the registered C program"""

# darrelops/services/build_service.py
import os
import subprocess
import logging
from darrelops.models import CProgramModel
from darrelops.extensions import db

def clone_repository(repo_url, clone_dir):
    """Clones the GitHub repository to the specified directory."""
    logger = logging.getLogger('BuildService')
    logger.info(f"Cloning repository {repo_url} into {clone_dir}")

    if os.path.exists(clone_dir):
        logger.info(f"Directory {clone_dir} already exists. Skipping clone.")
    else:
        try:
            result = subprocess.run(
                ["git", "clone", repo_url, clone_dir],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")
            logger.info(f"Repository cloned successfully: {result.stdout}")
        except Exception as e:
            logger.error(f"Failed to clone repository: {str(e)}")
            return False
    return True

def build_program(program: CProgramModel):
    logger = logging.getLogger('BuildService')

    # Step 1: Clone the repository
    clone_dir = os.path.join('repos', program.name)
    repo_cloned = clone_repository(program.repo_url, clone_dir)
    if not repo_cloned:
        logger.error(f"Failed to clone repository for program {program.name}")
        return False

    # Step 2: Update the build directory to the cloned repository
    program.build_dir = clone_dir

    # Log the files in the build directory
    files_in_build_dir = os.listdir(program.build_dir)
    logger.info(f"Files in build directory ({program.build_dir}): {files_in_build_dir}")

    # Step 3: Run the build command
    logger.info(f"Building program {program.name} with command {program.build_cmd} in directory {program.build_dir}.")
    try:
        result = subprocess.run(
            program.build_cmd.split(),
            cwd=program.build_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Build failed for program {program.name}: {result.stderr}")
            raise Exception(f"Build failed: {result.stderr}")
        
        logger.info(f"Build succeeded for program {program.name}: {result.stdout}")
        return True
    except Exception as e:
        logger.error(f"Build process encountered an exception: {str(e)}")
        return False

def check_for_new_commits():
    """Check all registed programs for new commits and triggers a build if new commits are found."""
    programs = CProgramModel.query.all()
    for program in programs:
        if not program.repo_url:
            continue
        
        # fetch latest commits
        repo_dir = os.path.join('repos', program.name)
        if os.path.exists(repo_dir):
            result = subprocess.run(
                ["git", "-C", repo_dir, "pull"],
                capture_output=True,
                text=True
            )
            if result.returncode == 0 and "Already up to date." not in result.stdout:
                # new commits found, trigger a build
                build_program(program)
            else:
                print(f"No new commits found for {program.name}.")
        else:
            print(f"Repository directory {repo_dir} not found.")
    