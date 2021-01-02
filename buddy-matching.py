import pandas 
import csv 
import random 

class Student:
	def __init__(self, name, year, on_campus, time_zone, meeting_freq, meeting_time, classes, major)
		self.name = name
		self.year = year
		self.on_campus = on_campus
		self.time_zone = time_zone
		self.meeting_time = meeting_time
		self.classes = classes
		self.major = major 

	def __eq__(self, other) : 
        return self.__dict__ == other.__dict__


compatability_scores = dict()

time_zones = {
	'UTC-12:00 International Date Line West' : 12,
	'UTC-11:00 Coordinated Universal Time-11': 13,
	'UTC-10:00 Aleutian Islands T': 14,
	'UTC-09:00 Alaska': 15,
	'UTC-08:00 Pacific Time':16,
	'UTC-07:00 Mountain Time': 17,
	'UTC-06:00 Central Time': 18,
	'UTC-05:00 Eastern Time': 19,
	'UTC-04:00 Atlantic Time': 20,
	'UTC-03:00 Brasilia': 21,
	'UTC-02:00 Coordinated Universal Time-02':22,
	'UTC-01:00 Azores': 23,
	'UTC-00:00 London': 0,
	'UTC+01:00 Berlin, Paris': 1,
	'UTC+02:00 Jerusalem': 2,
	'UTC+03:00 Moscow': 3,
	'UTC+04:00 Abu Dhabi': 4,
	'UTC+05:00 Islamabad': 5,
	'UTC+06:00 Astana': 6,
	'UTC+07:00 Bangkok, Jakarta': 7,
	'UTC+08:00 Beijing, Hong Kong': 8,
	'UTC+09:00 Tokyo, Osaka, Seoul': 9,
	'UTC+10:00 Guam': 10,
	'UTC+11:00 Chokurdakh': 11,
	'UTC+12:00 Coordinated Universal Time+12': 12,
	'UTC+13:00 Coordinated Universal Time+13': 13,
	'UTC+14:00 Coordinated Universal Time+14': 14,
}

meeting_frequency = {
	'Daily' = 1 
	'Weekly' = 2
	'Monthly' = 3
}

meeting_times= {
	'Morning 08:00-12:00' = 10
	'Afternoon 12:00-16:00' = 14
	'Evening 16:00- 20:00' = 18
	'Night 20:00- 24:00' = 22
}

def compute_similarity_score(student1, student2)
	score = 0
	num_classes_same = [value for value in student1.classes if value in student2.classes] 
	score = 0.25 *num_classes_same
	meeting_time1 = (student1.time_zone + student1.meeting_time)%24
	meeting_time2 = (student2.time_zone + student2.meeting_time)%24
	if abs(meeting_time1-meeting_time2) < 4:
		score = score
	else:
		score = abs(meeting_time1-meeting_time2) *0.1
	score = score - (student1.meeting_freq -student2.meeting_freq)*.1
	if student1.on_campus && student2.on_campus:
		score = score + 0.1 


def calculate_all_scores(students):
	compatability_scores = dict()
	for student1 in students:
		if student1.email not in compatability_scores:
			compatability_scores[student1.email] = dict()
		for student2 in students:
			if student2.email not in compatability_scores:
				compatability_scores[student2.email] = dict()
			if student1.email in compatability_scores[student2.email]:
				continue 
			if student1 == student2:
				continue 
			else:
				score = compute_similarity_score(student1,student2)
				compatability_scores[student1.email][student2.email] = score
				compatability_scores[student2.email][student1.email] = score
	return compatability_scores
def get_current_score(matches,scores):
	overall_score = 0 
	for match in matches:
		student1, student2 = match
		score = scores[student1][student2]
		overall_score +=score	
	return overall_score

def get_current_score(matches,scores):
	overall_score = 0 
	for match in matches:
		student1, student2 = match
		score = scores[student1][student2]
		overall_score +=score	
	return overall_score

def random_assign(students, scores):
	all_students = []
	for student in students:
		all_students.append(student)
	matches = []
	while all_students > 1:
		match1,match2 = random.sample(all_students,2)
		all_students.remove(match1)
		all_stuents.remvove(match2)
		matches.append([match1,match2])

def random_change(matches,scores):
	m1, m2 = random.sample(set(range(len(matches))), 2)
	match1 = matches[m1]
	match2 = matches[m2]
	current_score = get_current_score([match1,match2],scores)
	changed_match1 = [match1[0] +match2[1]]
	changed_match2 = [match1[1] +match2[0]]
	first_new_score = get_current_score([changed_match1,changed_match2],scores)
	changed_match3 = [match1[0] +match2[0]]
	changed_match4 = [match1[1] +match2[1]]
	second_new_score =  get_current_score([changed_match3,changed_match4],scores)
	if second_new_score > first_new_score && second_new_score > current_score:
		matches.remove(match1)
		matches.remove(match2)
		matches.append(changed_match3)
		matches.append(changed_match4)
	elif first_new_score > second_new_score && first_new_score > current_score:
		matches.remove(match1)
		matches.remove(match2)
		matches.append(changed_match1)
		matches.append(changed_match2)
	return matches


def main():
	## import data 
	student_data = pd.read_csv('Accountability Buddy Matching Survey  (Responses) - Form Responses 1.csv')
	students =  list()
	## Create list of students to compute compatability scores for each of the students
	for index, student in student_data.iterrows():
		name = student['Full Name']
		year = student['Year']
		on_campus = student['Will you be on-campus during the Spring term?']
		time_zone = student['Time Zone (Time Zone that you will be located in during the Spring term)']
		time_zone = time_zones[time_zone]
		meeting_freq = student['How often do you wish to meet?']
		meeting_freq = meeting_frequency[meeting_freq]
		meeting_time = student['Preferred Meeting Time']
		meeting_time = meeting_times[meeting_time]
		if on_campus == 'Yes'
			on_campus = True:
		else:
			on_campus = False 
		class1 = student['Accountability Courses: Please List courses for which you would want an accountability partner  [Class 1]']
		class2 = student['Accountability Courses: Please List courses for which you would want an accountability partner  [Class 2]']
		class2 = student['Accountability Courses: Please List courses for which you would want an accountability partner  [Class 3]']
		class4 = student['Accountability Courses: Please List courses for which you would want an accountability partner  [Class 4]']
		major = student['What is your Major?']
		classes = list(set({class1,class2,class3,class4}))
		newStudent = Student(name = name, year =year, 
			on_campus = on_campus,
			time_zone = time_zone,
			meeting_freq = meeting_freq,
			meeting_time = meeting_time,
			classes = classes,
			major = major)

		students.append(newStudent)
	best_score = positive_infnity = float('inf') 
	cacluate_scores = calculate_all_scores(students)



if __name__ == "__main__":
    main()