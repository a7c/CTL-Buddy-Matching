import pandas as pd
import csv 
import random 
from enum import Enum


class Student:
	def __init__(self, email, name, year, time_zone, meeting_freq, meeting_times, classes, major):
		self.email = email 
		self.name = name
		self.year = year
		self.time_zone = time_zone
		self.meeting_freq = meeting_freq
		self.meeting_times = meeting_times
		self.classes = classes
		self.major = major 

	def __eq__(self, other): 
		return self.__dict__ == other.__dict__

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
	'Daily': 1,
	'Weekly': 2,
	'Monthly': 3,
}

meeting_time_dict = {
	'Morning 08:00-12:00': 10, 
	'Afternoon 12:00-16:00': 14,
	'Evening 16:00- 20:00': 18,
	'Night 20:00- 24:00': 22,
}


major_types = {
	'Undeclared/Undecided': 0,
	'Aeronautics and Astronautics': 1,
	'African and African American Studies': 3, 
	'African Studies': 3, 
	'American Studies': 3, 
	'Anthropology': 3, 
	'Applied and Engineering Physics' :1 , 
	'Archaeology': 3, 
	'Architectural Design': 3, 
	'Art History': 4, 
	'Art Practice': 4, 
	'Asian American Studies': 3, 
	'Atmosphere/Energy': 1, 
	'Bioengineering': 1,
	'Biology': 2,
	'Biomechanical Engineering': 1,
	'Biomedical Computation': 2, 
	'Chemical Engineering': 1,
	'Chemistry': 2, 
	'Chicana/o - Latina/o Studies': 3, 
	'China Studies': 3, 
	'Civil and Environmental Engineering': 1,
	'Classics': 4, 
	'Communication': 4, 
	'Community Health and Prevention Research': 2, 
	'Comparative Literature': 4, 
	'Comparative Studies in Race and Ethnicity': 4, 
	'Computer Science' : 1,
	'Democracy, Development, and the Rule of Law': 3, 
	'Earth Systems': 2, 
	'Economics': 3, 
	'Education': 3, 
	'Electrical Engineering' : 1,
	'Energy Resources Engineering': 1,
	'Engineering Physics' : 1, 
	'English': 4, 
	'Environmental Systems Engineering': 1,
	'Ethics in Society': 3, 
	'Feminist, Gender, and Sexuality Studies': 3,
	'Film and Media Studies': 4, 
	'French': 4, 
	'Geological Studies': 2, 
	'Geophysics': 2, 
	'German Studies': 3,
	'History': 3, 
	'Honors in the Arts': 4,
	'Human Biology': 2, 
	'Iberian and Latin American Cultures': 3, 
	'International Policy Studies': 3, 
	'International Relations': 3, 
	'International Security Studies': 3, 
	'Italian': 4, 
	'Japanese': 4, 
	'Jewish Studies': 3, 
	'Korean': 4, 
	'Laboratory Animal Science': 2, 
	'Latin American Studies': 3, 
	'Linguistics': 4, 
	'Management Science and Engineering' : 1,
	'Materials Science and Engineering': 1,
	'Mathematical and Computational Science': 1,
	'Mathematics': 2, 
	'Mechanical Engineering': 1,
	'Modern Thought and Literature': 4,
	'Music': 4, 
	'Music, Science, and Technology': 2, 
	'Native American Studies': 3, 
	'Philosophy': 4, 
	'Philosophy and Religious Studies': 4,
	'Physics': 2, 
	'Political Science': 3, 
	'Product Design': 1,
	'Psychology': 2, 
	'Public Policy': 3, 
	'Religious Studies': 3, 
	'Science, Technology, and Society': 2, 
	'Slavic Languages and Literatures': 4, 
	'Sociology': 3, 
	'Spanish': 4, 
	'Statistics' : 2, 
	'Symbolic Systems': 1, 
	'Theater and Performance Studies': 4, 
	'Urban Studies': 3
}


compatability_scores = dict()

def compute_similarity_score(student1, student2):
	score = 0
	num_classes_same = [value for value in student1.classes if value in student2.classes] 
	score = 0.25 *len(num_classes_same)
	meeting_times1 = list(map(lambda mt: (student1.time_zone + mt) % 24, student1.meeting_times))
	meeting_times2 = list(map(lambda mt: (student2.time_zone + mt) % 24, student2.meeting_times))

	## simple pairwise comparison of both students' meeting times to see how close they can get
	meeting_time_diff_penalty = 3 # set to a "large" default value
	for time1 in meeting_times1:
		if meeting_time_diff_penalty == 0:
			break
		for time2 in meeting_times2:
			if abs(time1 - time2) < 4:
				meeting_time_diff_penalty = 0
				break
			else:
				meeting_time_diff_penalty = min(meeting_time_diff_penalty, abs(time1 - time2) * 0.1)
	score = score - meeting_time_diff_penalty
	score = score - (student1.meeting_freq -student2.meeting_freq)*.1
	diff_in_maj = abs(major_types[student1.major] - major_types[student2.major])
	score += (0.4- diff_in_maj*0.1)
	return score


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
		score = scores[student1.email][student2.email]
		overall_score +=score	
	return overall_score

def random_assign(students):
	all_students = []
	for student in students:
		all_students.append(student)
	matches = []
	while len(all_students) > 1:
		match1,match2 = random.sample(all_students,2)
		all_students.remove(match1)
		all_students.remove(match2)
		matches.append([match1,match2])
	return matches 

def random_change(matches,scores):
	m1, m2 = random.sample(set(range(len(matches))), 2)
	match1 = matches[m1]
	match2 = matches[m2]
	current_score = get_current_score([match1,match2],scores)
	changed_match1 = [match1[0] ,match2[1]]
	changed_match2 = [match1[1] ,match2[0]]
	first_new_score = get_current_score([changed_match1,changed_match2],scores)
	changed_match3 = [match1[0] ,match2[0]]
	changed_match4 = [match1[1] ,match2[1]]
	second_new_score =  get_current_score([changed_match3,changed_match4],scores)
	if second_new_score > first_new_score and second_new_score > current_score:
		matches.remove(match1)
		matches.remove(match2)
		matches.append(changed_match3)
		matches.append(changed_match4)
	elif first_new_score > second_new_score and first_new_score > current_score:
		matches.remove(match1)
		matches.remove(match2)
		matches.append(changed_match1)
		matches.append(changed_match2)
	return matches


def main():
	## import data 
	student_data = pd.read_csv('Accountability Buddy Matching Survey_January 12, 2021_21.06 - edited.csv')
	students =  list()
	student_data.rename(columns=lambda x: x.strip(),inplace=True)
	## Create list of students to compute compatability scores for each of the students
	for index, student in student_data.iterrows():
		name = student['Full Name'].strip()
		year = student['Year'].strip()
		email =  student['Email Address'].strip()
		time_zone = student['Time Zone (time zone where you will be located during Winter quarter)'].strip()
		time_zone = time_zones[time_zone]
		meeting_freq = student['How often do you wish to meet?'].strip()
		meeting_freq = meeting_frequency[meeting_freq]
		meeting_times = student['Preferred Meeting Time(s)'].strip().split(',')
		meeting_times = list(map(lambda mt: meeting_time_dict[mt], meeting_times))
		classes = student['Please select (up to four) courses for which you would want an accountability partner.'].strip().split(',')
		classes = list(set(classes)) # de-dupe
		major = student['Major'].strip()
		newStudent = Student(name = name, year =year, email = email,
			time_zone = time_zone,
			meeting_freq = meeting_freq,
			meeting_times = meeting_times,
			classes = classes,
			major = major)

		students.append(newStudent)
	best_score = float('inf') 
	compatability_scores = calculate_all_scores(students)
	matches = random_assign(students )
	current_score = get_current_score(matches,compatability_scores)
	num_rounds = 10 
	num_students = len(students)
	for i in range(num_rounds):
		for j in range(len(students)):
			matches = random_change(matches, compatability_scores)
		current_score = get_current_score(matches, compatability_scores)
		print('Current overall_score: ' + str(current_score))

	filename = "matches.csv"
	fields = ['Student 1', 'Student 2', 'Student 1 Email', 'Student 2 Email']

	write_matches = []
	for match in matches:
		write_matches.append([match[0].name,match[1].name,match[0].email,match[1].email])

	with open(filename, 'w') as csvfile:  
	    # creating a csv writer object  
	    csvwriter = csv.writer(csvfile)  
	        
	    # writing the fields  
	    csvwriter.writerow(fields)  
	        
	    # writing the data rows  
	    csvwriter.writerows(write_matches)





if __name__ == "__main__":
    main()