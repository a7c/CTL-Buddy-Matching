'''
Convert course info JSON files to a course list that can be pasted directly
into our Accountability Partner Program survey. 

Features:
- Deduplicates crosslisted courses
- Removes courses that are not relevant for us
  - e.g., ROTC courses, grad seminars, independent study
'''


import json
import os

from glob import glob
from functools import reduce

# dict to keep track of unique courses for deduping crosslisted courses
course_dict = {}


def flatten(t):
    return [item for sublist in t for item in sublist]


def course_to_formatted_string(c):
    return f'[{c["number"]}] {c["title"]}'


def should_keep_course(c):
    global course_dict
    if c['titleNoCrosslists'] in course_dict:
        return False
    course_dict[c['titleNoCrosslists']] = c
    return (
        # Filter out 400-level classes and above.
        # Need to account for classes with codes that contain letters
        int(''.join(ch for ch in c['code'] if ch.isdigit())) < 400 and
        # Filter out courses that can be taken for 0-1 credit
        0 not in c['units'] and
        1 not in c['units'] and
        # Filter out overseas courses
        "OSP" not in c['subject'] and
        # Filter out other non-relevant depts
        not any(str == c['subject']
                for str in [
                    'ARTSTUDI',
                    'CTS',
                    'EMED',
                    'FAMMED',
                    'GSBGEN',
                    'MED',
                    'NSUR',
                    'NENS',
                    'ORTHO',
                    'PATH',
                    'PEDS',
                    'RAD',
                    'RADO',
                    'RESPROG',
                    'ROTCAF',
                    'ROTCARMY',
                    'ROTCNAVY',
                    'SINY',
                    'SIW',
                    'SURG',
                    'UROL',
        ]) and
        # Filter out courses with certain keywords in the title
        not any(substr in c['title'].lower()
                for substr in [
            'independent study',
            'individual research',
            'workshop',
            'senior',
            'directed',
            'thesis'
            'practical training',
            'phd',
            'ph.d.',
            'colloquium',
            'dissertation',
            'capstone',
            "master's",
            'project',
            'graduate',
            'medical scholars research',
            'internship',
            'seminar',
            'special',
            'practicum',
            'honors research',
            'degree research',
            'reading group',
            'reading and research',
            'honors program',
            'tutorial',
            'topics',
            'qualifying',
            'orals',
            'clerkship',
            'elective',
            'grad',
            'orchestra',
            'ensemble',
            'thesis'
        ]) and
        # Filter out courses with certain keywords in the title
        (not any(substr in c['description'].lower()
                 for substr in [
            'class fee',
            'audition',
            'repeated for credit'
        ]) if c['description'] is not None else True)
    )


def main():
    files = [open(n, 'r') for n in glob('out/*.json')]
    data = flatten([json.loads(f.read()) for f in files])

    for course in data:
        try:
            course['titleNoCrosslists'] = course['title'][:course['title'].index(
                '(') - 1]
        except:
            course['titleNoCrosslists'] = course['title']
    filtered_data = filter(should_keep_course, data)
    formatted_course_list = [
        course_to_formatted_string(course) for course in filtered_data]
    course_list_str = reduce(lambda acc, s: acc +
                             "\n" + s, formatted_course_list)
    print(course_list_str)

    with open('course-list.txt', 'w') as f:
        f.write(course_list_str)


if __name__ == '__main__':
    main()
