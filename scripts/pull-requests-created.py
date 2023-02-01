import sys, json, utils

report = json.load(sys.stdin)
studentIDs = utils.loadUsernameDirectory(report)
alreadySeenPulls = []
for repository in report["repositories"]:
    pullRequests = utils.getAllPagesForQuery("/repos/" + repository + "/pulls?state=all&")
    for pull in pullRequests:
        if pull["id"] not in alreadySeenPulls:
            alreadySeenPulls.append(pull["id"])
            utils.safelyIncrement(report, "pull-requests-created", 1, pull["user"]["login"], studentIDs, repository)

print(json.dumps(report, indent=4))
