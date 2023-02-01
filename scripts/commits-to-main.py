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
            # Branch merges are't really "proper" code commits - count everything except those
            if "Merge pull request #" not in comment:
                username = utils.extractCommitter(commit)
                utils.safelyIncrement(report, "commits-to-main", 1, username, studentIDs, repository)

print(json.dumps(report, indent=4))
