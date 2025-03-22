import json

# Read the original JSON file
input_path = "/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/deps/python_repositories_with_lockfiles-manually-updated-pip.json"

with open(input_path, 'r') as f:
    data = json.load(f)

# Helper function to safely get dependencies count as int
def get_deps_count(repo):
    deps = repo.get("dependenciesCount", 0)
    if isinstance(deps, str):
        try:
            return int(deps)
        except ValueError:
            return 0
    return deps

# Filter and count repositories with PIP in projectType
pip_repos = {}

for repo_name, repo_info in data.items():
    project_types = repo_info.get("projectType", [])
    
    if "PIP" in project_types:
        pip_repos[repo_name] = repo_info

# Calculate statistics for PIP repositories
total_pip = len(pip_repos)
pip_deps_gt_0 = sum(1 for repo in pip_repos.values() if get_deps_count(repo) > 0)
pip_lockfile_exists = sum(1 for repo in pip_repos.values() if repo.get("lockfileExists") == True)
pip_deps_gt_0_lockfile = sum(1 for repo in pip_repos.values() 
                        if get_deps_count(repo) > 0 and repo.get("lockfileExists") == True)
pip_deps_gt_0_no_lockfile = sum(1 for repo in pip_repos.values() 
                           if get_deps_count(repo) > 0 and repo.get("lockfileExists") == False)
pip_lockfile_no_deps = sum(1 for repo in pip_repos.values() 
                      if repo.get("lockfileExists") == True and get_deps_count(repo) == 0)
pip_no_lockfile_no_deps = sum(1 for repo in pip_repos.values() 
                         if repo.get("lockfileExists") == False and get_deps_count(repo) == 0)

# Print statistics
print("PIP Statistics:")
print(f"Total PIP repositories: {total_pip}")
print(f"* dependencies > 0: {pip_deps_gt_0}")
print(f"* lockfile exists true: {pip_lockfile_exists}")
print(f"* dependencies > 0 and lockfile exists true: {pip_deps_gt_0_lockfile}")
print(f"* dependencies > 0 and lockfile exists false: {pip_deps_gt_0_no_lockfile}")
print(f"* lockfile exists true and dependencies = 0: {pip_lockfile_no_deps}")
print(f"* lockfile exists false and dependencies = 0: {pip_no_lockfile_no_deps}")