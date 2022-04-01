## Setup

`pip3 install xmltodict`

## Commands

First, update `fetch.py` to fetch from the appropriate quarter.

Then, run the following commands:
`python3 fetch.py -o raw`
`python3 parse.py -o out/ -p "raw/*.xml"`
`python3 gen-course-list.py`

The course list will be printed to console and written to the file `course-list.txt`.
