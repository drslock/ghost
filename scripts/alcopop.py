import sys, json, utils

import sys, json, utils

report = json.load(sys.stdin)
studentIDs = utils.loadUsernameDirectory(report)
for studentID in report["students"]:
    if "commits-to-main" not in report["students"][studentID]: report["students"][studentID]["ALCOPOP"] = "commits-to-main was not found"
    elif "aggregate-loc" not in report["students"][studentID]: report["students"][studentID]["ALCOPOP"] = "aggregate-loc was not found"
    elif report["students"][studentID]["commits-to-main"] == 0: report["students"][studentID]["ALCOPOP"] = 0
    else: report["students"][studentID]["ALCOPOP"] = round(report["students"][studentID]["aggregate-loc"] / report["students"][studentID]["commits-to-main"], 2)

print(json.dumps(report, indent=4))
