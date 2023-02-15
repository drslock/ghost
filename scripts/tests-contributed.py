import sys, json, utils

def isValidTestFilename(filename, extensions):
    for extension in testScriptExtensions:
        if file["path"].endswith(extension): return True
    return False

def getAggregateLOC(commit, targetFilename):
    aggregateLOC = 0
    if "Merge pull request #" not in commit["commit"]["message"]:
        commitDetails = utils.sendGetRequest(commit["url"])
        # Sometimes the details returned is just a string (rather than a JSON document)
        if type(commitDetails) != str:
            for change in commitDetails["files"]:
                # Make sure we only count the changes to the file we are interested in (the commit contains changes to many files !)
                if change["filename"] == targetFilename:
                    aggregateLOC += change["additions"]
                    aggregateLOC -= change["deletions"]
    return aggregateLOC

report = json.load(sys.stdin)
if len(sys.argv) > 1: testScriptExtensions = sys.argv[1:]
else: testScriptExtensions = [""]
studentIDs = utils.loadUsernameDirectory(report)
alreadySeenCommits = []
for repository in report["repositories"]:
    # Might have to request the "master" branch instead for some repositories
    mainBranch = utils.sendGetRequest("https://api.github.com/repos/" + repository + "/git/trees/main?")
    # Get the tree of all files in the main/master branch
    treeReport = utils.sendGetRequest("https://api.github.com/repos/" + repository + "/git/trees/" + mainBranch["sha"] + "?recursive=true")
    for file in treeReport["tree"]:
        # Look for filenames with "test" somewhere in the path (might want to refine this to "src/test" for Maven projects)
        if ("test" in file["path"].lower()) and (file["type"] != "tree"):
            if isValidTestFilename(file["path"], testScriptExtensions):
                print(file["path"])
                commits = utils.getAllPagesForQuery("/repos/" + repository + "/commits?path=" + file["path"] + "&")
                for commit in commits:
                    # Check that it's not an already seen commit (they get duplicated in different branches !)
                    if commit["url"] not in alreadySeenCommits:
                        alreadySeenCommits.append(commit["url"])
                        username = utils.extractCommitter(commit)
                        aggregateLOC = getAggregateLOC(commit, file["path"])
                        # Only count commits with a sensible number of lines of code (to stop "code dumps" or "code purges" skewing the data)
                        if (aggregateLOC > -500) and (aggregateLOC < 500):
                            print("  " + username + " " + str(aggregateLOC))
                            utils.safelyIncrement(report, "test-loc", aggregateLOC, username, studentIDs, repository)

# print(json.dumps(report, indent=4))
