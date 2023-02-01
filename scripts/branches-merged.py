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
            if "Merge pull request #" in comment:
                # GitHub doesn't always give us the login of a merge commit, so we have to hack it out of the email address !
                username = commit["commit"]["author"]["email"].split("+")[1].split("@")[0]
                utils.safelyIncrement(report, "branches-merged", 1, username, studentIDs, repository)

print(json.dumps(report, indent=4))
