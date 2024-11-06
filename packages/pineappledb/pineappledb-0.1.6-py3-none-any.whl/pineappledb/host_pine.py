import os
from twine import commands
from twine.utils import get_repository

def upload_package():
    # Define the directory containing the distribution files
    dist_directory = 'dist'

    # Check if the dist directory exists
    if not os.path.exists(dist_directory):
        print(f"Directory '{dist_directory}' does not exist. Please build your package first.")
        return

    # Get the repository URL (PyPI or TestPyPI)
    repository_url = "https://upload.pypi.org/legacy/"  # Change to TestPyPI URL if needed
    repository = get_repository(repository_url)

    # Prepare the distribution files
    distributions = [os.path.join(dist_directory, f) for f in os.listdir(dist_directory) if f.endswith(('.tar.gz', '.whl'))]

    if not distributions:
        print("No distribution files found in the 'dist' directory.")
        return

    # Upload the package using twine
    try:
        commands.upload(distributions, repository=repository)
        print("Package uploaded successfully.")
    except Exception as e:
        print(f"An error occurred while uploading: {e}")

if __name__ == "__main__":
    upload_package()