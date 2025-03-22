import json
import requests
import re
import base64
import os
import sys
import time

def count_pipenv_dependencies(json_file_path):
    """
    Count dependencies in Pipenv projects from a JSON file of GitHub repositories.
    
    Args:
        json_file_path: Path to the JSON file containing Pipenv project links
    """
    # Read the JSON file
    with open(json_file_path, 'r') as f:
        projects = json.load(f)
    
    # Set up GitHub API headers
    github_token = ""
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    # Process each project
    for project_name, project_data in projects.items():
        if 'PIP' in project_data.get('projectType', []):
            print(f"Processing Pipenv project: {project_name}")
            
            # Get repository contents
            repo_url = project_data['url']
            api_url = repo_url.replace('https://api.github.com/repos/', '')
            
            try:
                # Get the Pipfile content
                pipfile_url = f"https://api.github.com/repos/{api_url}/contents/Pipfile"
                response = requests.get(pipfile_url, headers=headers)
                response.raise_for_status()
                
                # API rate limit handling
                if int(response.headers.get('X-RateLimit-Remaining', 1)) < 5:
                    print("API rate limit nearly reached, sleeping...")
                    reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 3600))
                    sleep_time = max(reset_time - time.time(), 0) + 10
                    print(f"Sleeping for {sleep_time:.2f} seconds")
                    time.sleep(sleep_time)
                
                # Decode content
                file_content = base64.b64decode(response.json()['content']).decode('utf-8')
                
                # Count dependencies
                dependencies_count = 0
                
                # Look for dependencies in the [packages] section
                packages_match = re.search(r'\[packages\](.*?)(\[|\Z)', file_content, re.DOTALL)
                if packages_match:
                    packages_section = packages_match.group(1)
                    # Count lines that seem to be dependencies (not empty lines or comments)
                    packages_lines = [line.strip() for line in packages_section.split('\n') 
                                     if line.strip() and not line.strip().startswith('#') and "=" in line]
                    dependencies_count += len(packages_lines)
                
                # Look for dev dependencies in the [dev-packages] section
                dev_packages_match = re.search(r'\[dev-packages\](.*?)(\[|\Z)', file_content, re.DOTALL)
                if dev_packages_match:
                    dev_packages_section = dev_packages_match.group(1)
                    # Count lines that seem to be dependencies (not empty lines or comments)
                    dev_packages_lines = [line.strip() for line in dev_packages_section.split('\n') 
                                         if line.strip() and not line.strip().startswith('#') and "=" in line]
                    dependencies_count += len(dev_packages_lines)
                
                # Add the count to the project data
                project_data['dependenciesCount'] = dependencies_count
                print(f"Found {dependencies_count} dependencies in {project_name}")
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching Pipfile for {project_name}: {e}")
                project_data['dependenciesCount'] = -1  # Indicate error
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
    
    # Write the updated JSON back to the file
    with open(json_file_path, 'w') as f:
        json.dump(projects, f, indent=2)
    
    print(f"Processing complete. Updated {json_file_path}")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python pipenv_dependency_counter.py <json_file_path>")
    #     sys.exit(1)
    
    count_pipenv_dependencies("/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/deps/python_repositories_with_lockfiles.json")