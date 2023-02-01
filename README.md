# GitHub Organisation Surveyor and Tabulator (GHOST)

## Overview

This repository contains a suite of python scripts to interrogate GitHub organisations
and report on the contributions made by individual developers. The aim of these scripts
is to simplify the process of assessing group projects by providing markers with transparency
into the work performed by each student.

- `issues-assigned` Reports the number of issues that have been _assigned_ to each student
- `issues-completed` Reports the number of issues that have been _completed_ each student
- `commits-to-main` Lists the number of commits made by students (to the main/master branch only)
- `pull-requests-created` Extracts the number of pull requests made by each student
- `branches-merged` Reports the number of branches merged into the main/master branch by a student
- `aggregate-loc` Total _increase_ in the number of lines of code from all commits by a student
- `alcopop` Average Lines of Code Per Orchestrated Push (i.e. `aggregate-loc/commits-to-main`)

Note that the `alcopop` script requires both the `commits-to-main` and `aggregate-loc` scripts
to have been run previously (so that the required data is available).

## Report format

The JSON report document contains details of the organisation and repository names,
as well as the UoB student IDs, students real names and GitHub usernames (note that each
student may have more than one GitHub username). An example JSON report document is shown below:

```JSON
{
    "repositories": [ "uob/examplerepository" ],
    "students": {
        "aa11111": { "real-name": "Dave Daverson", "usernames": ["davey"] },
        "bb22222": { "real-name": "Alan Allanson", "usernames": ["al123"] },
        "cc33333": { "real-name": "Steve Stevenson", "usernames": ["stevie"] },
        "dd44444": { "real-name": "Chris Christerson", "usernames": ["chrissy"] }
    }
}
```

## Usage

Each command reads in a JSON document from stdin, augments it with data extracted from GitHub and
then prints the result back out to stdout.

The any number of scripts can be chained together using pipes

For example, the following command passes an unpopulated student report into the issues-assigned

cat students.json | python issues-assigned.py | python commits-to-main.py  > output.json


## Document Format Conversion

Two additional scripts for

csv2json
json2csv
