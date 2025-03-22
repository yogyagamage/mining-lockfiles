import json

# Read the original JSON file
input_path = "/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/deps/jsts_repositories_with_lockfiles-filtered-new.json"
input_path2 = "/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/deps/jsts_repositories_with_lockfiles.json"
output_path = "/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/deps/jsts_repositories_with_lockfiles-filtered-new2.json"

with open(input_path, 'r') as f:
    data = json.load(f)
with open(input_path2, 'r') as f:
    data2 = json.load(f)

# Helper function to safely get dependencies count as int
def get_deps_count(repo):
    deps = repo.get("dependenciesCount", 0)
    if isinstance(deps, str):
        try:
            return int(deps)
        except ValueError:
            return -1
    return deps

# Filter and count repositories
pnpm_repos = {}
npm_repos = {}

for repo_name, repo_info in data.items():
    project_types = repo_info.get("projectType", [])
    
    if "PNPM" in project_types and get_deps_count(repo_info) != -1:
        pnpm_repos[repo_name] = repo_info
        
    if "NPM" in project_types and get_deps_count(repo_info) != -1:
        npm_repos[repo_name] = repo_info
    
for repo_name, repo_info in data2.items():
    project_types = repo_info.get("projectType", [])   
    if "npm" in project_types and get_deps_count(repo_info) != -1:
        npm_repos[repo_name] = repo_info

# PNPM Statistics
total_pnpm = len(pnpm_repos)
pnpm_deps_gt_0 = sum(1 for repo in pnpm_repos.values() if get_deps_count(repo) > 0)
pnpm_deps_gt_0_no_lockfile = sum(1 for repo in pnpm_repos.values() 
                           if get_deps_count(repo) > 0 and repo.get("lockfileExists") == False)
pnpm_no_lockfile = sum(1 for repo in pnpm_repos.values() if repo.get("lockfileExists") == False)
pnpm_no_lockfile_no_deps = sum(1 for repo in pnpm_repos.values() 
                         if repo.get("lockfileExists") == False and get_deps_count(repo) == 0)
pnpm_deps_gt_0_lockfile = sum(1 for repo in pnpm_repos.values() 
                        if get_deps_count(repo) > 0 and repo.get("lockfileExists") == True)
pnpm_lockfile_no_deps = sum(1 for repo in pnpm_repos.values() 
                      if repo.get("lockfileExists") == True and get_deps_count(repo) == 0)
pnpm_lockfile_lock = sum(1 for repo in pnpm_repos.values() 
                      if repo.get("lockfileExists") == True)
pnpm_lockfile_lock_dep = sum(1 for repo in pnpm_repos.values() 
                         if repo.get("lockfileExists") == True and get_deps_count(repo) > 0)

# NPM Statistics
total_npm = len(npm_repos)
npm_deps_gt_0 = sum(1 for repo in npm_repos.values() if get_deps_count(repo) > 0)
npm_deps_gt_0_no_lockfile = sum(1 for repo in npm_repos.values() 
                           if get_deps_count(repo) > 0 and repo.get("lockfileExists") == False)
npm_no_lockfile = sum(1 for repo in npm_repos.values() if repo.get("lockfileExists") == False)
npm_no_lockfile_no_deps = sum(1 for repo in npm_repos.values() 
                         if repo.get("lockfileExists") == False and get_deps_count(repo) == 0)
npm_deps_gt_0_lockfile = sum(1 for repo in npm_repos.values() 
                        if get_deps_count(repo) > 0 and repo.get("lockfileExists") == True)
npm_lockfile_no_deps = sum(1 for repo in npm_repos.values() 
                      if repo.get("lockfileExists") == True and get_deps_count(repo) == 0)
npm_lockfile_lock = sum(1 for repo in npm_repos.values() 
                      if repo.get("lockfileExists") == True )
npm_lockfile_lock_dep = sum(1 for repo in npm_repos.values() 
                         if repo.get("lockfileExists") == True and get_deps_count(repo) > 0)

# Save filtered data (you can choose which subset to save, or both)
filtered_data = {**pnpm_repos, **npm_repos}  # Combine both
with open(output_path, 'w') as f:
    json.dump(filtered_data, f, indent=2)

# Print statistics
print("PNPM Statistics:")
print(f"Total PNPM repositories: {total_pnpm}")
print(f"PNPM repos with dependenciesCount > 0: {pnpm_deps_gt_0}")
print(f"PNPM repos with dependenciesCount > 0 and lockfileExists = false: {pnpm_deps_gt_0_no_lockfile}")
print(f"PNPM repos with lockfileExists = false: {pnpm_no_lockfile}")
print(f"PNPM repos with lockfileExists = false and dependenciesCount = 0: {pnpm_no_lockfile_no_deps}")
print(f"PNPM repos with dependenciesCount > 0 and lockfileExists = true: {pnpm_deps_gt_0_lockfile}")
print(f"PNPM repos with lockfileExists = true and dependenciesCount = 0: {pnpm_lockfile_no_deps}")
print(f"PNPM repos with lockfileExists = true : {pnpm_lockfile_lock}")
print(f"PNPM repos with lockfileExists = true and dep > 0 : {pnpm_lockfile_lock_dep}")

print("\nNPM Statistics:")
print(f"Total NPM repositories: {total_npm}")
print(f"NPM repos with dependenciesCount > 0: {npm_deps_gt_0}")
print(f"NPM repos with dependenciesCount > 0 and lockfileExists = false: {npm_deps_gt_0_no_lockfile}")
print(f"NPM repos with lockfileExists = false: {npm_no_lockfile}")
print(f"NPM repos with lockfileExists = false and dependenciesCount = 0: {npm_no_lockfile_no_deps}")
print(f"NPM repos with dependenciesCount > 0 and lockfileExists = true: {npm_deps_gt_0_lockfile}")
print(f"NPM repos with lockfileExists = true and dependenciesCount = 0: {npm_lockfile_no_deps}")
print(f"NPM repos with lockfileExists = true : {npm_lockfile_lock}")
print(f"NPM repos with lockfileExists = true and dep > 0 : {npm_lockfile_lock_dep}")