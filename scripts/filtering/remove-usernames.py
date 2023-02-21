import sys, json

report = json.load(sys.stdin)

# Remove usernames from list of students in full report
if "students" in report:
    for studentID in report["students"]:
        nextStudent = report["students"][studentID]
        del nextStudent["usernames"]

# Remove usernames if report just contains a list of students
for studentID in report:
    nextStudent = report[studentID]
    if "usernames" in nextStudent:
        del nextStudent["usernames"]

print(json.dumps(report, indent=4))
