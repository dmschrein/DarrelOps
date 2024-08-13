import os
import shutil

def remove_file(file_path):
    """Remove a file if it exists."""
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed file: {file_path}")
    else:
        print(f"File not found: {file_path}")

def remove_directory(dir_path):
    """Remove a directory and its contents if it exists."""
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
        print(f"Removed directory: {dir_path}")
    else:
        print(f"Directory not found: {dir_path}")

def reset_program():
    """Reset the program by removing specific files and directories."""
    # Paths to remove
    database_path = 'darrelops/artifactory/database.db'
    artifactory_path = 'darrelops/artifactory/'
    repos_path = 'darrelops/repos'
    

    # Remove the database file
    remove_file(database_path)

    # Remove the artifactory directory
    remove_directory(artifactory_path)

    # Remove the repos directory
    remove_directory(repos_path)

    print("Program reset completed.")

if __name__ == '__main__':
    reset_program()
