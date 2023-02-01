import sys, json, utils

report = { "repositories": [], "students": {} }
lines = sys.stdin.readlines()
for line in lines:
    tokens = line.split(",")
    studentID = tokens[0].strip()
    realName = tokens[1].strip()
    report["students"][studentID] = {"real-name": realName, "usernames":[]}
    for i in range(2, len(tokens)):
        nextUsername = tokens[i].strip()
        if len(nextUsername) > 0: report["students"][studentID]["usernames"].append(nextUsername)
print(json.dumps(report, indent=4))
