import sys, json

report = json.load(sys.stdin)
populatedStudents = {}
if "repositories" in report: del report["repositories"]
for studentID in report["students"]:
    nextStudent = report["students"][studentID]
    if len(nextStudent) > 2: populatedStudents[studentID] = nextStudent
report["students"] = populatedStudents
print(json.dumps(report, indent=4))
