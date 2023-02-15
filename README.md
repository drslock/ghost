# GitHub Organisation Surveyor and Tabulator (GHOST)

## Overview

This repository contains a selection of python scripts to interrogate GitHub organisations
and report back on the contributions made by individual developers. The aim of these scripts
is to simplify the process of assessing group projects by providing markers with transparency
into the work performed by each student.

- `issues-assigned` Reports the number of issues that have been _assigned_ to each student
- `issues-completed` Reports the number of issues that have been _completed_ by each student
- `commits-per-week` Lists the number of commits students have made each week _that have reached the master branch_
- `commits-to-main` The total number of commits made by students _that have reached the master branch_
- `pull-requests-created` Extracts the number of pull requests made by each student
- `branches-merged` Reports the number of branches merged into the main/master branch by a student
- `tests-contributed` Report the number of lines of test code contributed by a student
- `aggregate-loc` Extracts the total _increase_ in number of lines of code from all commits by a student
- `alcopop` Calculates "**A**verage **L**ines of **Co**de **P**er **O**rchestrated **P**ush" (i.e. `aggregate-loc`/`commits-to-main`)

The `tests-contributed` script will count the number of lines in any file containing "test" in the pathname.
An optional list of test file extensions can be specified when running this script in order to
filter out any non-test file types. For example:
```
python tests-contributed.py .java .py
```
will only count the lines of code added to `.java` and `.py` files (with "test" in the pathname).

Note that the `alcopop` script requires both the `commits-to-main` and `aggregate-loc` scripts
to have previously been run (so that the required data is available to calculate the average).

**Warning**: Due to the nature of analysis in `aggregate-loc` script (which has to interrogate
_every_ commit which has pushed to a repository) this script can take a long time to complete.

## Authentication

In order to run the scripts, you will need to create a personal access token on the
[GitHub Website](https://github.com/settings/tokens) with the following permissions:
- "Full control of private repositories"
- "Full control of orgs and teams, read and write org projects"
- "Read ALL user profile data"
- "Read and write team discussions"
- "Full control of projects"

The generated access token should be inserted into a file called `credentials.secret` and stored
in the root folder of GHOST.

## Report document format

The JSON report document contains details of the organisation and repository names,
as well as details regarding each student (UoB student IDs, students real names and GitHub usernames).
An example JSON report document is shown below:

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

At then end of the JSON report document, there may appear an additional `spectres` section.
This contains the usernames of any unknown contributors encountered during the analysis of the GitHub
repositories (i.e. usernames not listed in the `students` section of the report). It is worth
spending some time reviewing these unknown usernames to see if it is worth updating the student
entries to include them (otherwise students may not get the full credit for their contributions).

## Usage

Each python script reads in a JSON report document from stdin, augments it with data extracted from
GitHub and then prints out an updated version of the report back out to stdout.

Reports can be run one-at-a-time, with the result being stored in intermediate documents.
For example:
```
cat empty-report.json | python issues-assigned.py > issues-report.json
```
Followed by:
```
cat issues-report.json | python commits-to-main.py > issues-report.json
```
Alternatively, any number of scripts can be chained together using pipes, for example:
```
cat students.json | python issues-assigned.py | python commits-to-main.py  > output.json
```

## Document Format Conversion

In addition to the core data analysis scripts, there are two document format conversion scripts:
- `csv2json` Converts a CSV spreadsheet (containing just Student ID, real name and GitHub usernames) in an initial JSON report
- `json2csv` Converts a JSON report already populated with data into a CSV spreadsheet
