import sys, json, utils

report = json.load(sys.stdin)
studentIDs = utils.loadUsernameDirectory(report)
alreadySeenIssues = []
for repository in report["repositories"]:
    issues = utils.getAllPagesForQuery("/repos/" + repository + "/issues?state=closed&")
    for issue in issues:
        if issue["id"] not in alreadySeenIssues:
            alreadySeenIssues.append(issue["id"])
            for assignee in issue["assignees"]:
                utils.safelyIncrement(report, "issues-completed", 1, assignee["login"], studentIDs, repository)

print(json.dumps(report, indent=4))
