import math
import pandas
import random
import sys

from functools import reduce
from itertools import takewhile

import shared

FRESHMAN = 0
SOPHOMORE = 1
JUNIOR = 2
SENIOR = 3
year_to_string = {
    0: "Freshman",
    1: "Sophomore",
    2: "Junior",
    3: "Senior"
}

EMPTY_WEIGHTS = [0, 0, 0, 0]

FORBIDDEN_SPECIALIZATIONS = [
    'ENGR'
]

TIME_ZONES = list(shared.time_zones.keys())
# just guessing how likely it is that students will be in certain time zones
TIME_ZONE_WEIGHTS_IF_OFF_CAMPUS = [
    0,
    0,
    1,
    2,
    20,
    5,
    10,
    20,
    2,
    2,
    0,
    1,
    5,
    5,
    3,
    3,
    3,
    3,
    3,
    5,
    10,
    5,
    2,
    1,
    0,
    0,
    0
]


def take_digits(str):
    return int(''.join(takewhile(str.isdigit, st)))

# we need custom comparison functions to make sure that 99 < 100A, for example. 
class CourseNumber:
    def __init__(self, num):
        self.num = num
    def __repr__(self):
        return str(self.num)
    def __lt__(self, number2):
        digits = int(''.join(takewhile(str.isdigit, str(self.num))))
        digits2 = int(''.join(takewhile(str.isdigit, str(number2))))
        # if the digits are equal, we use string comparison
        if (digits == digits2):
            return str(self.num) < str(number2)
        else:
            return digits < digits2
    def __le__(self, number2):
        return self.num == number2 or self.__lt__(number2)
    def __gt__(self, number2):
        digits = int(''.join(takewhile(str.isdigit, str(self.num))))
        digits2 = int(''.join(takewhile(str.isdigit, str(number2))))
        # if the digits are equal, we use string comparison
        if (digits == digits2):
            return str(self.num) > str(number2)
        else:
            return digits > digits2
    def __ge__(self, number2):
        return self.num == number2 or self.__gt__(number2)

class CourseCode: 
    def __init__(self, dept, number):
        self.dept = dept
        self.number = number
    def __repr__(self):
        return self.dept + " " + str(self.number)

class Course:
    def __init__(self, name, course_codes, weights, weight_multiplier):
        self.name = name
        self.course_codes = course_codes
        self.weights = weights
        self.weight_multiplier = weight_multiplier
    def __repr__(self):
        return self.name + " " + str(self.course_codes) + " " + str(self.weights) + " (evals: " + str(self.weight_multiplier) + ")"
    def set_weights(self, weights):
        self.weights = weights

def parse_course_codes(raw_course):
    course_codes = [CourseCode(raw_course['dept'], CourseNumber(raw_course['number']))]
    maybe_course_codes = [
        (raw_course['dept 2'], raw_course['number 2']),
        (raw_course['dept 3'], raw_course['number 3']),
        (raw_course['dept 4'], raw_course['number 4']),
        (raw_course['dept 5'], raw_course['number 5']),
    ] 
    for (dept, number) in maybe_course_codes:
        if not pandas.isna(dept) and not pandas.isna(number):
            course_codes.append(CourseCode(dept, CourseNumber(number)))
    return course_codes

def parse_course_data(filename):
    # parse course data from csv
    course_data = pandas.read_csv(filename)
    courses = list()
    for i, course in course_data.iterrows():
        name = course['course name']
        course_codes = parse_course_codes(course)
        # some courses have few (or 0) evals so we set the multiplier to 10 in
        # to give them at least some chance of showing up when we randomly select
        # classes
        weight_multiplier = max(course['evals'], 10)
        # these weights could be NaN if the course has no listed year distribution
        weight_freshman = math.sqrt(weight_multiplier * course['freshman'])
        weight_sophomore = math.sqrt(weight_multiplier * course['sophomore'])
        weight_junior = math.sqrt(weight_multiplier * course['junior'])
        weight_senior = math.sqrt(weight_multiplier * course['senior'])
        weights = [weight_freshman, weight_sophomore, weight_junior, weight_senior]
        courses.append(
            Course(
                name = name, 
                course_codes = course_codes,
                weights = weights,
                weight_multiplier = weight_multiplier
            )
        )
    return courses

def compute_average_weights(courses):
    sum_weights = list(EMPTY_WEIGHTS)
    sum_weight_multipliers = 0
    num_courses_counted = 0
    for course in courses:
        if not pandas.isna(course.weights[0]):
            sum_weights = [
                sum_weights[0] + course.weights[0],
                sum_weights[1] + course.weights[1],
                sum_weights[2] + course.weights[2],
                sum_weights[3] + course.weights[3]
            ]
            sum_weight_multipliers = sum_weight_multipliers + course.weight_multiplier
            num_courses_counted = num_courses_counted + 1
    avg_weights = list(map(lambda w: w / num_courses_counted, sum_weights))
    # we need this value to normalize weights later
    avg_weight_multiplier = sum_weight_multipliers / num_courses_counted
    return (avg_weights, avg_weight_multiplier)

def generate_weights_for_unweighted_courses(courses, avg_weights, avg_weight_multiplier):
    for course in courses:
        if pandas.isna(course.weights[0]):
            # we examine all the crosslistings of a course before settling on a weight
            numbers = list(map(lambda c: c.number, course.course_codes))
            min_course_num = reduce(min, numbers)
            max_course_num = reduce(max, numbers)
            weights = list([0, 0, 0, 0])
            # courses aimed at underclassmen
            if max_course_num < CourseNumber(100):
                weights = [
                    avg_weights[FRESHMAN] * 2,
                    avg_weights[SOPHOMORE] * 1.2,
                    avg_weights[JUNIOR] * 0.6,
                    avg_weights[SENIOR] * 0.2
                ]
            # courses aimed at undergrads
            elif min_course_num >= CourseNumber(100) and max_course_num < CourseNumber(200):
                weights = [
                    avg_weights[FRESHMAN] * 0.7,
                    avg_weights[SOPHOMORE] * 1.4,
                    avg_weights[JUNIOR] * 1.1,
                    avg_weights[SENIOR] * 0.5,
                    # small grad student attendance
                ]
            elif min_course_num >= CourseNumber(200) and max_course_num < CourseNumber(300):
                weights = [
                    avg_weights[FRESHMAN] * 0.2,
                    avg_weights[SOPHOMORE] * 0.6,
                    avg_weights[JUNIOR] * 1.3,
                    avg_weights[SENIOR] * 1.2,
                    # medium grad student attendance
                ]
            elif min_course_num >= CourseNumber(300):
                weights = [
                    avg_weights[FRESHMAN] * 0,
                    avg_weights[SOPHOMORE] * 0.2,
                    avg_weights[JUNIOR] * 0.7,
                    avg_weights[SENIOR] * 2,
                    # large grad student attendance
                ]
            elif min_course_num >= CourseNumber(0) and max_course_num < CourseNumber(200):
                weights = [
                    avg_weights[FRESHMAN] * 1.2,
                    avg_weights[SOPHOMORE] * 1.2,
                    avg_weights[JUNIOR] * 1,
                    avg_weights[SENIOR] * 0.3,
                    # small grad student attendance
                ]
            elif min_course_num >= CourseNumber(100) and max_course_num < CourseNumber(300):
                weights = [
                    avg_weights[FRESHMAN] * 0.3,
                    avg_weights[SOPHOMORE] * 0.9,
                    avg_weights[JUNIOR] * 1.1,
                    avg_weights[SENIOR] * 0.9,
                    # large grad student attendance
                ]
            else:
                # let's not bother making up heuristics for other possibilities
                weights = list(avg_weights)
            # normalize the calculated weight values and then multiply by the
            # course's weight multiplier
            weights = list(map(lambda w: w / avg_weight_multiplier * course.weight_multiplier, weights))
            course.set_weights(weights)

def compute_total_weights(courses):
    total_weights = list(EMPTY_WEIGHTS)
    for course in courses:
        total_weights = [
            total_weights[0] + course.weights[0],
            total_weights[1] + course.weights[1],
            total_weights[2] + course.weights[2],
            total_weights[3] + course.weights[3]
        ]
    return total_weights

def select_random_course_weighted(courses, year):
    return random.choices(
        courses,
        list(map(lambda c: c.weights[year], courses))
    )[0]

# turns a list of course codes into a list of strings with department strings only
def map_course_codes_to_depts(course):
    return list(map(lambda code: code.dept, course.course_codes))

# warning: mutates `courses`
def maybe_select_specialization(courses, selected_courses, year, total_weights):
    # freshmen and sophomores might have a major, juniors and seniors almost definitely do
    if (
        year == FRESHMAN and random.randrange(0, 3) == 0
        or year == SOPHOMORE and random.randrange(0, 2) == 0
        or year == JUNIOR
        or year == SENIOR
    ):
        specialization = random.choices(map_course_codes_to_depts(selected_courses[0]))[0]
        # if we chose a specialization, re-weight the courses to make it
        # much more likely that we choose courses in our dept
        if (specialization != None):
            total_weight_of_preferred_courses = 0
            for course in courses:
                if specialization in map_course_codes_to_depts(course):
                    total_weight_of_preferred_courses += course.weights[year]

            # balance weights so that there's ~50% chance of choosing from
            # our dept
            weight_diff = total_weights[year] - total_weight_of_preferred_courses
            for course in courses:
                if specialization not in map_course_codes_to_depts(course):
                    course.weights[year] = course.weights[year] / weight_diff * total_weight_of_preferred_courses
        if specialization not in FORBIDDEN_SPECIALIZATIONS:
            return specialization
        else:
            return None
    else:  
        return None

def generate_student(name, courses, total_weights):
    # copy `courses` so we can mutate it safely.
    courses = list(courses)

    # randomly choose a year for the student. these options are weighted to
    # reflect our more likely students.
    year = random.choice([
        FRESHMAN,
        FRESHMAN,
        FRESHMAN,
        FRESHMAN,
        SOPHOMORE,
        SOPHOMORE,
        SOPHOMORE,
        JUNIOR,
        JUNIOR,
        SENIOR
    ])
    specialization = None
    selected_courses = [select_random_course_weighted(courses, year)]

    # randomly choose up to 5 courses total.
    # also, at random, choose a specialization (aka a department/major). 
    # a student of a certain specialization is more likely to choose courses
    # from that department.

    # select a second course
    if (random.randrange(0, 5) > 0):
        specialization = maybe_select_specialization(courses, selected_courses, year, total_weights)
        selected_courses.append(select_random_course_weighted(courses, year))
        # select a third course
        if (random.randrange(0, 5) > 1):
            if (specialization == None):
                specialization = maybe_select_specialization(courses, selected_courses, year, total_weights)
            selected_courses.append(select_random_course_weighted(courses, year))
            # select a fourth course
            if (random.randrange(0, 5) > 2):
                if (specialization == None):
                    specialization = maybe_select_specialization(courses, selected_courses, year, total_weights)
                selected_courses.append(select_random_course_weighted(courses, year))
                # select a fourth course
                if (random.randrange(0, 5) > 3):
                    if (specialization == None):
                        specialization = maybe_select_specialization(courses, selected_courses, year, total_weights)
                    selected_courses.append(select_random_course_weighted(courses, year))

    # de-dupe
    selected_courses = list(set(list(selected_courses)))

    on_campus = random.choice(["Yes", "No"])
    time_zone = 'UTC-08:00 Pacific Time'
    if on_campus == "No":
        time_zone = random.choices(TIME_ZONES, TIME_ZONE_WEIGHTS_IF_OFF_CAMPUS)[0]

    student = shared.Student(
        name,
        year_to_string[year],
        on_campus,
        time_zone,
        random.choice(list(shared.meeting_frequency.keys())),
        random.choice(list(shared.meeting_times.keys())),
        list(map(lambda c: str(c.course_codes) + " " + str(c.name), selected_courses)),
        str(specialization)
    )

    print(student.name)
    print("- Year: " + student.year)
    print("- On campus? " + student.on_campus)
    print("- Timezone: " + student.time_zone)
    print("- Meeting freq: " + student.meeting_freq)
    print("- Meeting time: " + student.meeting_time)
    print("- Major: " + student.major)
    print("- Classes:")
    for course in student.classes:
        print("-- " + course)
    print()

    return student

def main():
    courses = parse_course_data('course-data.csv')

    # calculate average weight of all non-NaN weights. each course has different
    # weights assigned to each class year in order to reflect year distribution
    # among classes
    (avg_weights, avg_weight_multiplier) = compute_average_weights(courses)
    
    # assign weights to courses with no year distributions, based on the
    # average weights so far and course info. mutates the objects in `courses`.
    generate_weights_for_unweighted_courses(courses, avg_weights, avg_weight_multiplier)

    total_weights = compute_total_weights(courses)

    num_students_to_generate = 1
    if len(sys.argv) > 1:
        num_students_to_generate = int(float(sys.argv[1]))

    students = list()
    for i in range(num_students_to_generate):
        students.append(generate_student('Student ' + str(i), courses, total_weights))


if __name__ == '__main__':
    main()