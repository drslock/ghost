import sys, json, utils

report = json.load(sys.stdin)
studentIDs = utils.loadUsernameDirectory(report)
for repository in report["repositories"]:
    contributors = utils.sendGetRequest("https://api.github.com/repos/" + repository + "/stats/contributors?")
    for contributor in contributors:
        username = contributor["author"]["login"]
        weeklyContributions = contributor["weeks"]
        # Weekly contributions are most-recent-first, so flip them before adding to the report
        weeklyContributions.reverse()
        for week in weeklyContributions:
            utils.safelyAppend(report, "commits-per-week", str(week["c"]) + ",", username, studentIDs, repository)

print(json.dumps(report, indent=4))
