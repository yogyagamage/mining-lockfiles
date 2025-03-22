import json

# Read the original JSON file
input_path = "/Users/yogyagamage/Documents/UdeM/lockfiles/lockfile-miner/output/bun_repositories_with_lockfiles.json"

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

# Function to calculate stats for a given set of repositories
def calculate_stats(repos):
   total = len(repos)
   deps_gt_0 = sum(1 for repo in repos.values() if get_deps_count(repo) > 0)
   lockfile_exists = sum(1 for repo in repos.values() if repo.get("lockfileExists") == True)
   deps_gt_0_lockfile = sum(1 for repo in repos.values() 
                       if get_deps_count(repo) > 0 and repo.get("lockfileExists") == True)
   deps_gt_0_no_lockfile = sum(1 for repo in repos.values() 
                          if get_deps_count(repo) > 0 and repo.get("lockfileExists") == False)
   lockfile_no_deps = sum(1 for repo in repos.values() 
                     if repo.get("lockfileExists") == True and get_deps_count(repo) == 0)
   no_lockfile_no_deps = sum(1 for repo in repos.values() 
                        if repo.get("lockfileExists") == False and get_deps_count(repo) == 0)
   
   return {
       "total": total,
       "dependencies > 0": deps_gt_0,
       "lockfile exists true": lockfile_exists,
       "dependencies > 0 and lockfile exists true": deps_gt_0_lockfile,
       "dependencies > 0 and lockfile exists false": deps_gt_0_no_lockfile,
       "lockfile exists true and dependencies = 0": lockfile_no_deps,
       "lockfile exists false and dependencies = 0": no_lockfile_no_deps
   }

# Initialize dictionaries for each project type
yarn_repos = {}
bun_repos = {}
npm_repos = {}  # this will handle both "NPM" and "npm"
pnpm_repos = {}
multi_type_repos = {}
all_repos = {}
all_other_repos = {}

# Process repositories
for repo_name, repo_info in data.items():
   project_types = repo_info.get("projectType", [])
   
   # Check if repo has multiple project types
   if len(project_types) > 1:
       multi_type_repos[repo_name] = repo_info
   
   # Add repo to respective type dictionaries
   if "YARN" in project_types and not ("npm" in project_types or "NPM" in project_types or "PNPM" in project_types):
       yarn_repos[repo_name] = repo_info
       
   if "BUN" in project_types and not ("npm" in project_types or "NPM" in project_types or "PNPM" in project_types):
       bun_repos[repo_name] = repo_info
       
   if "NPM" in project_types or "npm" in project_types:
       npm_repos[repo_name] = repo_info
       
   if "PNPM" in project_types:
       pnpm_repos[repo_name] = repo_info
    
   if ("NPM" in project_types or "PNPM" in project_types):
       if (repo_info.get("lockfileExists") == False):
           print(repo_name)
       all_other_repos[repo_name] = repo_info
    
   all_repos[repo_name] = repo_info
    

# Calculate statistics for each type
yarn_stats = calculate_stats(yarn_repos)
bun_stats = calculate_stats(bun_repos)
npm_stats = calculate_stats(npm_repos)
pnpm_stats = calculate_stats(pnpm_repos)
multi_type_stats = calculate_stats(multi_type_repos)
all_stats = calculate_stats(all_repos)
all_other_stats = calculate_stats(all_other_repos)

# Print statistics
def print_stats(name, stats):
   print(f"\n{name} Statistics:")
   print(f"Total repositories: {stats['total']}")
   print(f"* dependencies > 0: {stats['dependencies > 0']}")
   print(f"* lockfile exists true: {stats['lockfile exists true']}")
   print(f"* dependencies > 0 and lockfile exists true: {stats['dependencies > 0 and lockfile exists true']}")
   print(f"* dependencies > 0 and lockfile exists false: {stats['dependencies > 0 and lockfile exists false']}")
   print(f"* lockfile exists true and dependencies = 0: {stats['lockfile exists true and dependencies = 0']}")
   print(f"* lockfile exists false and dependencies = 0: {stats['lockfile exists false and dependencies = 0']}")

print_stats("YARN", yarn_stats)
print_stats("BUN", bun_stats)
print_stats("NPM", npm_stats)
print_stats("PNPM", pnpm_stats)
print_stats("Multi-Type", multi_type_stats)
print_stats("all", all_stats)
print_stats("all_other", all_other_stats)

# Print count of specific combinations if needed
yarn_bun = sum(1 for repo in data.values() 
              if "YARN" in repo.get("projectType", []) and "BUN" in repo.get("projectType", []))
yarn_npm = sum(1 for repo in data.values() 
              if "YARN" in repo.get("projectType", []) and 
              ("NPM" in repo.get("projectType", []) or "npm" in repo.get("projectType", [])))
yarn_pnpm = sum(1 for repo in data.values() 
               if "YARN" in repo.get("projectType", []) and "PNPM" in repo.get("projectType", []))
bun_npm = sum(1 for repo in data.values() 
             if "BUN" in repo.get("projectType", []) and 
             ("NPM" in repo.get("projectType", []) or "npm" in repo.get("projectType", [])))
bun_pnpm = sum(1 for repo in data.values() 
              if "BUN" in repo.get("projectType", []) and "PNPM" in repo.get("projectType", []))
npm_pnpm = sum(1 for repo in data.values() 
              if ("NPM" in repo.get("projectType", []) or "npm" in repo.get("projectType", [])) and 
              "PNPM" in repo.get("projectType", []))

print("\nCombination Counts:")
print(f"YARN + BUN: {yarn_bun}")
print(f"YARN + NPM: {yarn_npm}")
print(f"YARN + PNPM: {yarn_pnpm}")
print(f"BUN + NPM: {bun_npm}")
print(f"BUN + PNPM: {bun_pnpm}")
print(f"NPM + PNPM: {npm_pnpm}")