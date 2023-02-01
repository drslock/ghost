import sys, json, utils

report = json.load(sys.stdin)
studentIDs = utils.loadUsernameDirectory(report)
alreadySeenCommits = []
for repository in report["repositories"]:
    commits = utils.getAllPagesForQuery("/repos/" + repository + "/commits?")
    for commit in commits:
        # Check that it's not an already seen commit (they get duplicated in different branches !)
        if commit["url"] not in alreadySeenCommits:
            alreadySeenCommits.append(commit["url"])
            comment = commit["commit"]["message"]
            if "Merge pull request #" not in commit["commit"]["message"]:
                if "login" in commit["committer"]:
                    username = commit["committer"]["login"]
                    aggregateLOC = 0
                    commitDetails = utils.sendGetRequest(commit["url"])
                    for change in commitDetails["files"]:
                        aggregateLOC += change["additions"]
                        aggregateLOC -= change["deletions"]
                    # Only count commits with a sensible number of lines of code (to stop "code dumps" or "code purges" skewing the data)
                    if (aggregateLOC > -500) and (aggregateLOC < 500):
                        utils.safelyIncrement(report, "aggregate-loc", aggregateLOC, username, studentIDs, repository)

print(json.dumps(report, indent=4))
