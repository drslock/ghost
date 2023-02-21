import sys, json, utils
from time import sleep

report = json.load(sys.stdin)
studentIDs = utils.loadUsernameDirectory(report)
alreadySeenCommits = []
for repository in report["repositories"]:
    # Sleep between each repo, so that we don't over-use the API and get throttled
    sleep(60)
    commits = utils.getAllPagesForQuery("/repos/" + repository + "/commits?")
    for commit in commits:
        # Check that it's not an already seen commit (they get duplicated in different branches !)
        if commit["url"] not in alreadySeenCommits:
            alreadySeenCommits.append(commit["url"])
            username = utils.extractCommitter(commit)
            aggregateLOC = 0
            if "Merge pull request #" not in commit["commit"]["message"]:
                commitDetails = utils.sendGetRequest(commit["url"])
                # Sometimes the details returned is just a string (rather than a JSON document)
                if type(commitDetails) != str:
                    for change in commitDetails["files"]:
                        aggregateLOC += change["additions"]
                        aggregateLOC -= change["deletions"]
            # Only count commits with a sensible number of lines of code (to stop "code dumps" skewing the data)
            if (aggregateLOC > 0) and (aggregateLOC < 500):
                utils.safelyIncrement(report, "aggregate-loc", aggregateLOC, username, studentIDs, repository)

print(json.dumps(report, indent=4))
