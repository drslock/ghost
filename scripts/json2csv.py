import sys, json, utils

report = json.load(sys.stdin)
columnHeadings = []

# First get all of the column headings
for studentID in report["students"]:
    for feature in report["students"][studentID]:
        if feature not in columnHeadings: columnHeadings.append(feature)
print("Student ID, " + ", ".join(columnHeadings))

# Now loop through all the students and print out their personal stats
for studentID in report["students"]:
    print(studentID, end=", ")
    studentRecord = report["students"][studentID]
    for feature in columnHeadings:
        if feature in studentRecord:
            # if the feature is an array, then print out all the elements
            if type(studentRecord[feature])==list: print("/".join(studentRecord[feature]), end=", ")
            else: print(studentRecord[feature], end=", ")
        else: print("0,", end="")
    print()
