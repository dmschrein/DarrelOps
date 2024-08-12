"""Service to build the registered C program"""

# darrelops/services/build_service.py
import os
import subprocess
import logging

# build the C program
def build_program(program):
    from darrelops.services import package_artifact
    logger = logging.getLogger('BuildService')

    # Clone the repository
    clone_dir = os.path.join('repos', program['name'])
    repo_cloned = clone_repository(program['repo_url'], clone_dir)
    if not repo_cloned:
        logger.error(f"Failed to clone repository for program {program['name']}")
        return False

    # Update the build directory to the cloned repository
    program['build_dir'] = clone_dir

    # Log the files in the build directory
    files_in_build_dir = os.listdir(program['build_dir'])
    logger.info(f"Files in build directory ({program['build_dir']}): {files_in_build_dir}")

    # Step 3: Run the build command
    logger.info(f"Building program {program['name']} with command {program['build_cmd']} in directory {program['build_dir']}.")
    try:
        result = subprocess.run(
            program.build_cmd.split(),
            cwd=program.build_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            logger.error(f"Build failed for program {program['name']}: {result.stderr}")
            raise Exception(f"Build failed: {result.stderr}")
        
        logger.info(f"Build succeeded for program {program['name']}: {result.stdout}")
        
        # Step 4: Package the artifact
        artifact_path = package_artifact(program)
        logger.info(f"Artifact packaged at {artifact_path}")
        return artifact_path
    
    except Exception as e:
        logger.error(f"Build process encountered an exception: {str(e)}")
        return False

# clone repositories
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

def check_for_new_commits(app):
    """Check all registed programs for new commits and triggers a build if new commits are found."""
    from darrelops.utils.config import load_programs

    logger = logging.getLogger('Build Service: checking for new commits')
    
    with app.app_context():
        
        programs = load_programs()
        for program in programs:
            logger.info(f"Checking for new commits for program {program['name']}...")
            
            if not program.repo_url:
                continue
            
            # fetch latest commits
            repo_dir = os.path.join('repos', program['name'])
            if os.path.exists(repo_dir):
                try:
                    result = subprocess.run(
                        ["git", "-C", repo_dir, "pull"],
                        capture_output=True,
                        text=True
                    )
                    if result.returncode == 0 and "Already up to date." not in result.stdout:
                        # new commits found, trigger a build
                        logger.info(f"New commits found for {program['name']}. Rebuilding...")
                        build_program(program)
                    else:
                        print(f"No new commits found for {program['name']}.")
                except Exception as e:
                    logger.error(f"Failed to pull latest commits for {program['name']}: {str(e)}")
            else:
                logger.warning(f"Repository directory {repo_dir} does not exist.")
                print(f"Repository directory {repo_dir} not found.")
        