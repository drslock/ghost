import requests

def loadUsernameDirectory(report):
    studentIDs = {}
    for studentID in report["students"].keys():
        for username in report["students"][studentID]["usernames"]:
            studentIDs[username] = studentID
    return studentIDs

def extractCommitter(commit):
    # GitHub doesn't always give us the login of a commit, so sometimes we have to hack it out of the email address !
    if ("author" in commit) and (commit["author"] is not None) and ("login" in commit["author"]): return commit["author"]["login"]
    else: return commit["commit"]["committer"]["email"].split("@")[0]

def safelyIncrement(report, featureName, amount, username, studentIDs, repoName):
    studentRecord = getStudentRecordByUsername(report, username, studentIDs, repoName)
    if studentRecord is not None:
        if featureName not in studentRecord: studentRecord[featureName] = 0
        studentRecord[featureName] += amount

def safelyAppend(report, featureName, amount, username, studentIDs, repoName):
    studentRecord = getStudentRecordByUsername(report, username, studentIDs, repoName)
    if studentRecord is not None:
        if featureName not in studentRecord: studentRecord[featureName] = ""
        studentRecord[featureName] += amount

def getStudentRecordByUsername(report, username, studentIDs, repoName):
    if username in studentIDs:
        id = studentIDs[username]
        return report["students"][id]
    # If we DON'T know who the student is, record the fact in the report
    elif ("github-actions" not in username) and ("web-flow" not in username):
        if "spectres" not in report: report["spectres"] = []
        userPlusRepoName = username + "@" + repoName
        if(userPlusRepoName not in report["spectres"]): report["spectres"].append(userPlusRepoName)
        return None

def getAllPagesForQuery(query):
    allResults = []
    pageNumber = 0
    nextBatch = sendGetRequest("https://api.github.com" + query + "per_page=100&page=" + str(pageNumber))
    while (len(nextBatch) > 0):
        allResults.extend(nextBatch)
        pageNumber += 1
        nextBatch = sendGetRequest("https://api.github.com" + query + "per_page=100&page=" + str(pageNumber))
    return allResults

def sendGetRequest(url):
    accessToken = open("credentials.secret").read().split("\n")[0]
    headers = {"Authorization": "token " + accessToken, "Accept": "application/vnd.github.v3+json"}
    response = requests.get(url, headers=headers)
    if (response.status_code == 200): return response.json()
    else: return ""
