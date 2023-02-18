import sys, json

def toInt(value):
    if (type(value) == int) or (type(value) == float): return value
    else: return 0;

report = json.load(sys.stdin)
for studentID in report["students"]:
    warnings = ""
    for feature in report["students"][studentID]:
        value = report["students"][studentID][feature]
        if (feature == "issues-completed") and (toInt(value) < 20): warnings += "#"
        if (feature == "commits-to-main") and (toInt(value) < 20): warnings += "#"
        if (feature == "ALCOPOP") and (toInt(value) < 10): warnings += "#"
    print(warnings + "\t" + report["students"][studentID]["real-name"])
