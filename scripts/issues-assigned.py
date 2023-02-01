import sys, json, utils

report = json.load(sys.stdin)
studentIDs = utils.loadUsernameDirectory(report)
alreadySeenIssues = []
for repository in report["repositories"]:
    issues = utils.getAllPagesForQuery("/repos/" + repository + "/issues?state=all&")
    for issue in issues:
        if issue["id"] not in alreadySeenIssues:
            alreadySeenIssues.append(issue["id"])
            for assignee in issue["assignees"]:
                utils.safelyIncrement(report, "issues-assigned", 1, assignee["login"], studentIDs, repository)

print(json.dumps(report, indent=4))
