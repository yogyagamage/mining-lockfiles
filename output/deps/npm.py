import json
import requests
import base64
import os
import sys
import time

def count_npm_dependencies(json_file_path):
    """
    Count dependencies in npm projects from a JSON file of GitHub repositories.
    
    Args:
        json_file_path: Path to the JSON file containing npm project links
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
        if 'YARN' in project_data.get('projectType', []) or 'BUN' in project_data.get('projectType', []):
            print(f"Processing npm project: {project_name}")
            
            # Get repository contents
            repo_url = project_data['url']
            api_url = repo_url.replace('https://api.github.com/repos/', '')
            
            try:
                # Get the package.json file content
                package_url = f"https://api.github.com/repos/{api_url}/contents/package.json"
                response = requests.get(package_url, headers=headers)
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
                
                # Parse JSON
                package_json = json.loads(file_content)
                
                # Count dependencies
                dependencies_count = 0
                
                # Count main dependencies
                if 'dependencies' in package_json:
                    dependencies_count += len(package_json['dependencies'])
                
                # Count dev dependencies
                if 'devDependencies' in package_json:
                    dependencies_count += len(package_json['devDependencies'])
                
                # Count peer dependencies
                if 'peerDependencies' in package_json:
                    dependencies_count += len(package_json['peerDependencies'])
                
                # Count optional dependencies
                if 'optionalDependencies' in package_json:
                    dependencies_count += len(package_json['optionalDependencies'])
                
                # Add the count to the project data
                project_data['dependenciesCount'] = dependencies_count
                print(f"Found {dependencies_count} dependencies in {project_name}")
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching package.json for {project_name}: {e}")
                project_data['dependenciesCount'] = -1  # Indicate error
            except json.JSONDecodeError as e:
                print(f"Error parsing package.json for {project_name}: {e}")
                project_data['dependenciesCount'] = -1  # Indicate error
            
            # Add a small delay to avoid rate limiting
            time.sleep(1)
    
    # Write the updated JSON back to the file
    with open("/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/bun_repositories_with_lockfiles.json", 'w') as f:
        json.dump(projects, f, indent=2)
    
    print(f"Processing complete. Updated {json_file_path}")

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python npm_dependency_counter.py <json_file_path>")
    #     sys.exit(1)
    
    count_npm_dependencies("/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/deps/jsts_repositories_with_lockfiles.json")