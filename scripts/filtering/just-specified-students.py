import sys, json

report = json.load(sys.stdin)
specifiedStudents = {}
if "repositories" in report: del report["repositories"]
for studentID in report["students"]:
    if studentID in sys.argv: specifiedStudents[studentID] = report["students"][studentID]
report["students"] = specifiedStudents
print(json.dumps(report, indent=4))
