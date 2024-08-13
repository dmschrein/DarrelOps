"""Service to build the registered C program"""

# darrelops/services/build_service.py
import datetime
import os
import subprocess
import logging
from darrelops.models import CProgramModel, BuildStatusModel
from darrelops.extensions import db, app

def clone_repository(repo_url, clone_dir):
    """Clones the GitHub repository to the specified directory."""
    logger = logging.getLogger('BuildService')
    logger.info(f"Cloning repository {repo_url} into {clone_dir}")

    if os.path.exists(clone_dir):
        logger.info(f"Directory {clone_dir} already exists. Pulling the latest commits...")
        try:
            result = subprocess.run(
                ["git", "-C", clone_dir, "pull"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"Git pull failed: {result.stderr}")
            logger.info(f"Repository updated with most recent commits successfully: {result.stdout}")
        except Exception as e:
            logger.error(f"Failed to pull latest commits: {str(e)}")
            return False
    else:
        logger.info(f"Directory {clone_dir} does not exists. Cloning repository {repo_url} into {clone_dir}...")
        try:
            result = subprocess.run(
                ["git", "clone", repo_url, clone_dir],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")
            logger.info(f"Repository updated with most recent commits successfully: {result.stdout}")
        except Exception as e:
            logger.error(f"Failed to pull latest commits: {str(e)}")
            return False
    return True


def save_build_status(program, commit_hash, status, log):
    """Saves the build status to the database."""
    if not program or not program.id:
        raise ValueError("Invalid program or program ID")
    
    new_status = BuildStatusModel(
        program_id=program.id,
        commit_hash=commit_hash,
        status=status,
        timestamp=datetime.datetime.now(datetime.timezone.utc),
        log=log
    )
    db.session.add(new_status)
    db.session.commit()

# build C program
def build_program(program: CProgramModel):
    logger = logging.getLogger('BuildService')

    # Step 1: Clone the repository
    clone_dir = os.path.join('repos', program.name)
    repo_cloned = clone_repository(program.repo_url, clone_dir)
    if not repo_cloned:
        logger.error(f"Failed to clone repository for program {program.name}")
        return False
    
    # Step 2: Get the latest commit hash
    try:
        latest_commit = subprocess.check_output(
            ["git", "-C", clone_dir, "rev-parse", "HEAD"]
        ).strip().decode('utf-8')
    except Exception as e:
        logger.error(f"Failed to retrieve latest commit hash: {str(e)}")
        save_build_status(program, None, 'failed', 'Failed to retrieve latest commit hash')
        return False

    # Update the build directory to the cloned repository
    program.build_dir = clone_dir

    # Log the files in the build directory
    files_in_build_dir = os.listdir(program.build_dir)
    logger.info(f"Files in build directory ({program.build_dir}): {files_in_build_dir}")
    
     # Step 4: Run the build command
    logger.info(f"Building program {program.name} with command {program.build_cmd} in directory {program.build_dir}.")
    save_build_status(program, latest_commit, 'building', 'Build started')

    try:
        result = subprocess.run(
            program.build_cmd.split(),
            cwd=program.build_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Build failed for program {program.name}: {result.stderr}")
            save_build_status(program, latest_commit, 'failed', result.stderr)
            return False
        

        logger.info(f"Build succeeded for program {program.name}: {result.stdout}")
        save_build_status(program, latest_commit, 'completed', result.stdout)

        # Save the latest commit hash to the program model
        program.latest_commit = latest_commit
        db.session.commit()  # Save changes to the database

        return True
    except Exception as e:
        logger.error(f"Build process encountered an exception: {str(e)}")
        save_build_status(program, latest_commit, 'failed', str(e))
        return False

def check_for_new_commits():
    """Check all registed programs for new commits and triggers a build if new commits are found."""
    logger = logging.getLogger('Build Service: checking for new commits')
    
    with app.app_context():
        programs = CProgramModel.query.all()
        for program in programs:
            logger.info(f"Checking for new commits for program {program.name}...")
            
            if not program.repo_url:
                continue
            
            # Define the repository directory
            repo_dir = os.path.join('repos', program.name)
            
            if os.path.exists(repo_dir):
                try:
                    # Fetch the latest commits without merging
                    subprocess.run(["git", "-C", repo_dir, "fetch"], check=True)
                    
                    # Get the latest commit hash from the remote branch
                    remote_commit = subprocess.check_output(
                        ["git", "-C", repo_dir, "rev-parse", "origin/main"]
                    ).strip()
                    
                    # Get the latest commit hash from the local branch
                    local_commit = subprocess.check_output(
                        ["git", "-C", repo_dir, "rev-parse", "HEAD"]
                    ).strip()

                    if local_commit != remote_commit:
                        # New commits found
                        logger.info(f"New commits found for {program.name}. Rebuilding...")
                        build_program(program)
                    else:
                        logger.info(f"No new commits found for {program.name}.")
                except Exception as e:
                    logger.error(f"Failed to check for new commits for {program.name}: {str(e)}")
            else:
                logger.warning(f"Repository directory {repo_dir} does not exist.")