import json
import requests
import re
import base64
import os
import time

def filter_python_projects(json_file_path):
    """
    Filter Python projects from a JSON file of GitHub repositories:
    - Check each repository for pyproject.toml to identify Poetry projects
    - Filter PIP projects based on existing metadata
    
    Args:
        json_file_path: Path to the JSON file containing Python project links
    """
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        projects = json.load(f)
    
    # Set up GitHub API headers
    github_token = ""
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    # Prepare filtered project dictionaries
    poetry_projects = {}
    pip_projects = {}
    
    # Process each project
    project_count = len(projects)
    current_project = 0
    
    for project_name, project_data in projects.items():
        current_project += 1
        print(f"Processing project {current_project}/{project_count}: {project_name}")
        
        # Check if it's already identified as a PIP project
        if 'PIP' in project_data.get('projectType', []):
            pip_projects[project_name] = project_data
        
        # Get repository contents
        repo_url = project_data['url']
        api_url = repo_url.replace('https://api.github.com/repos/', '')
        
        try:
            # Get the pyproject.toml content
            pyproject_url = f"https://api.github.com/repos/{api_url}/contents/pyproject.toml"
            response = requests.get(pyproject_url, headers=headers)
            
            # API rate limit handling
            remaining_requests = int(response.headers.get('X-RateLimit-Remaining', 1))
            if remaining_requests < 5:
                print("API rate limit nearly reached, sleeping...")
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
                sleep_time = max(reset_time - time.time(), 0) + 10
                print(f"Sleeping for {sleep_time:.2f} seconds")
                time.sleep(sleep_time)
            
            # Check if pyproject.toml exists
            if response.status_code == 200:
                # Decode content
                file_content = base64.b64decode(response.json()['content']).decode('utf-8')
                
                # Check if it's a Poetry project
                if '[tool.poetry]' in file_content or '[tool.poetry.dependencies]' in file_content:
                    print(f"Found Poetry project: {project_name}")
                    # Update project type to include POETRY
                    if 'projectType' in project_data:
                        if 'POETRY' not in project_data['projectType']:
                            project_data['projectType'].append('POETRY')
                    else:
                        project_data['projectType'] = ['POETRY']
                    
                    # Add to poetry projects
                    poetry_projects[project_name] = project_data
        
        except requests.exceptions.RequestException as e:
            print(f"Error checking pyproject.toml for {project_name}: {e}")
        
        # Add a small delay to avoid rate limiting
        time.sleep(1)
    
    # Write the filtered projects to separate files
    output_dir = os.path.dirname(json_file_path)
    
    # Write poetry projects
    poetry_output_path = os.path.join(output_dir, 'poetry_filtered.json')
    with open(poetry_output_path, 'w') as f:
        json.dump(poetry_projects, f, indent=2)
    
    # Write pip projects
    pip_output_path = os.path.join(output_dir, 'pip_filtered.json')
    with open(pip_output_path, 'w') as f:
        json.dump(pip_projects, f, indent=2)
    
    print(f"Processing complete.")
    print(f"Found {len(poetry_projects)} Poetry projects, saved to {poetry_output_path}")
    print(f"Found {len(pip_projects)} PIP projects, saved to {pip_output_path}")

if __name__ == "__main__":
    json_file_path = "/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/deps/python_repositories_with_lockfiles-manually-updated-pip.json"
    filter_python_projects(json_file_path)