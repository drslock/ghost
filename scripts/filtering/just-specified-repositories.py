import sys, json

requestedRepositories = []
report = json.load(sys.stdin)
allRepositories = report["repositories"]
for repoName in sys.argv:
    for repository in allRepositories:
        if repoName in repository: requestedRepositories.append(repository)
report["repositories"] = requestedRepositories

print(json.dumps(report, indent=4))
