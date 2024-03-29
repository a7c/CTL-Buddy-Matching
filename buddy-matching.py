import pandas as pd
import csv 
import random 
from enum import Enum

import shared

compatability_scores = dict()

def compute_similarity_score(student1, student2):
	score = 0
	num_classes1 = len(student1.classes)
	num_classes2 = len(student2.classes)
	num_classes_check = min(num_classes1,num_classes2)
	if num_classes_check == 1:
		weight = 1
	elif num_classes_check == 2:
		weight = 0.5
	elif num_classes_check == 3:
		weight = 0.75
	else:
		weight = 0.25
	num_classes_same = [value for value in student1.classes if value in student2.classes] 
	score = weight *len(num_classes_same)
	meeting_times1 = list(map(lambda mt: (student1.time_zone + mt) % 24, student1.meeting_times))
	meeting_times2 = list(map(lambda mt: (student2.time_zone + mt) % 24, student2.meeting_times))

	if student1.partner_type == student2.partner_type:
		score = score+0.25
	elif student1.partner_type == 3 or student2.partner_type == 3 :
		score = score+0.15

	if student1.meeting_type == student2.meeting_type and(student1.meeting_type ==1 or student1.meeting_type ==3) :
		score = score+0.25
	elif student1.meeting_type == 2 or student2.meeting_type == 2 :
		score = score+0.15


	num_sim_work_types = 0
	for work_type in student1.meeting_work_type:
		if work_type in student2.meeting_work_type:
			num_sim_work_types+=1

	score = score+ .1*num_sim_work_types

	## simple pairwise comparison of both students' meeting times to see how close they can get
	meeting_time_diff_penalty = 5 # set to a "large" default value
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
	score = score - abs(student1.meeting_freq -student2.meeting_freq)*.10
	diff_in_maj = abs(shared.major_types[student1.major] - shared.major_types[student2.major])
	diff_in_year = abs(student1.year - student2.year)
	score += (0.4- diff_in_maj*0.15)
	score += (0.4- diff_in_year*0.05)
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

def assign_last_student(matches,last_student):
	best_score = 0 
	index = 0 
	index_of_assign = 0
	for match in matches:
		score1 = compute_similarity_score(match[0], last_student)
		score2 = compute_similarity_score(match[0], last_student)
		avg_score = (score1 +score2)/2
		if avg_score > best_score:
			index_of_assign = index
			best_score = avg_score
		index+=1 
	return index_of_assign


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
	if len(all_students) == 1:
		last_student = all_students[0]
		return matches, last_student
	return matches, None

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

def get_in_common2(student1, student2):
	classes_same = [value for value in student1.classes if value in student2.classes] 
	return classes_same

def get_in_common3(student1, student2, student3):
	classes_same1 = [value for value in student1.classes if value in student2.classes] 
	classes_same2 = [value for value in classes_same1 if value in student3.classes] 
	return classes_same2
def main():
	## import data 
	student_data = pd.read_csv('Accountability Partner Program - Undergraduate Matching Survey (Fall 2021)_October 10, 2021_14.14.csv')
	students =  list()
	student_data.rename(columns=lambda x: x.strip(),inplace=True)
	## Create list of students to compute compatability scores for each of the students

	## To prevent people from signing up twice
	## if they sign up twice we take the most up to date version 
	sunet_to_student = dict()
	for index, student in student_data.iterrows():
		name = student[shared.q_full_name].strip()
		year = student[shared.q_year].strip()
		year = shared.year_type[year]
		email =  student[shared.q_email_address].strip().lower()
		time_zone_str = student[shared.q_time_zone].strip()
		time_zone = shared.time_zones[time_zone_str]
		##meeting_freq_str = student[shared.q_meeting_freq].strip()
		##meeting_freq = shared.meeting_frequency[meeting_freq_str]
		meeting_freq_str = student[shared.q_meeting_freq].strip()
		meeting_freq = int(student[shared.q_meeting_freq].strip().split(' ')[0])
		meeting_types_of_work_str = str(student[shared.q_types_of_work])
		if meeting_types_of_work_str != 'nan':
			meeting_work_type = list(meeting_types_of_work_str.split(','))
		else:
			meeting_types_of_work_str = []

		meeting_type_str = student[shared.q_meeting_type].strip()
		meeting_type = shared.meeting_type[meeting_type_str]
			
		partner_type_str = student[shared.q_partner_type].strip()
		partner_type = shared.partner_type[partner_type_str]
		meeting_times_str = student[shared.q_meeting_times].strip()
		meeting_times = student[shared.q_meeting_times].strip().split(',')
		meeting_times = list(map(lambda mt: shared.meeting_times[mt], meeting_times))
		sunet = student[shared.q_sunet].strip()
		phone = str(student[shared.q_phone]).strip()
		if phone =='nan':
			phone = 'Not Provided'
		classes = student[shared.q_classes].strip()#.split(',[')
		if len(classes.split(',[')) > 1:
			final_classes = []
			index = 0 
			for class_ in classes.split(',['):
				if index == 0:
					final_classes.append(class_)
				else:
					final_classes.append(str('['+class_))
				index+=1
			classes = list(set(final_classes)) # de-dupe
		else:
			classes = [classes]

		major = student[shared.q_major].strip()
		newStudent = shared.Student(name = name, year =year, email = email,
			time_zone = time_zone,
			time_zone_str = time_zone_str,
			meeting_freq_str = meeting_freq_str, 
			meeting_freq = meeting_freq,
			meeting_work_type = meeting_work_type,
			partner_type = partner_type,
			meeting_type = meeting_type,
			meeting_times = meeting_times,
			meeting_times_str = meeting_times_str,
			phone = phone, 
			partner_type_str=partner_type_str,
			classes = classes,
			major = major)
		sunet_to_student[sunet] = newStudent
	best_score = float('inf') 
	students = list(sunet_to_student.values())
	
	## FIRST ROUND
	compatability_scores = calculate_all_scores(students)
	matches,last_student = random_assign(students )
	current_score = get_current_score(matches,compatability_scores)
	num_rounds = 200 
	num_students = len(students)
	for i in range(num_rounds):
		for j in range(len(students)):
			matches = random_change(matches, compatability_scores)
		current_score = get_current_score(matches, compatability_scores)
	print('Current overall_score: ' + str(current_score))

	## NEXT ROUNDS 
	num_initialize = 200
	best_matches = matches
	best_score = current_score
	for i in range(num_initialize):
		matches, last_student = random_assign(students )
		current_score = get_current_score(matches,compatability_scores)
		num_rounds = 200 
		num_students = len(students)
		for i in range(num_rounds):
			for j in range(len(students)):
				matches = random_change(matches, compatability_scores)
			current_score = get_current_score(matches, compatability_scores)
		if current_score > best_score:
			best_matches = matches
			best_score = current_score
		if i %100 == 0:
			print('Current best: ' + str(best_score))
	print('Current best: ' + str(best_score))
	filename = "matches3.csv"
	fields = ['Student 1', 'Student 2','Student 3', 'Student 1 Email', 'Student 2 Email','Student 3 Email',
	'Classes in Common', 'Student Major 1', 'Student Major 2', 'Student Major 3',
	'Student 1 Time Zone','Student 2 Time Zone', 'Student 3 Time Zone',
	'Student 1 Meeting Frequency','Student 2 Meeting Frequency', 'Student 3 Meeting Frequency',
	'Student 1 Buddy Type','Student 2 Buddy Type', 'Student 3 Buddy Type',
	'Student 1 Type of Work','Student 2 Type of Work', 'Student 3 Type of Work',
	'Student 1 Meeting Times','Student 2 Meeting Times', 'Student 3 Meeting Times',
	'Student 1 Phone', 'Student 2 Phone','Student 3 Phone',
	'Student 1 Preferred Meeting Type', 'Student 2 Preferred Meeting Type','Student 3 Preferred Meeting Type',]

	if last_student is not None:
		print(last_student)
		index_of_assign = assign_last_student(matches,last_student)
		matches[index_of_assign].append(last_student)
	write_matches = []
	inv_map = {v: k for k, v in shared.time_zones.items()}
	inv_map_meeting_type = {v: k for k, v in shared.meeting_type.items()}
	for match in matches:
		if len(match) == 2:
			write_matches.append([match[0].name,match[1].name,' ' ,
				match[0].email,match[1].email, ' ',
				str(get_in_common2(match[0],match[1])),
				match[0].major,match[1].major, ' ',
				inv_map[match[0].time_zone],inv_map[match[1].time_zone], ' ',
				match[0].meeting_freq_str,match[1].meeting_freq_str, ' ',
				match[0].partner_type_str,match[1].partner_type_str, ' ',
				', '.join(match[0].meeting_work_type),', '.join(match[1].meeting_work_type), ' ',
				match[0].meeting_times_str,match[1].meeting_times_str, ' ',
				match[0].phone,match[1].phone, ' ',
				inv_map_meeting_type[match[0].meeting_type],inv_map_meeting_type[match[1].meeting_type], ' ',
				])
		else:
			write_matches.append([match[0].name,match[1].name,match[2].name ,
				match[0].email,match[1].email, match[2].email,
				str(get_in_common3(match[0],match[1],match[2])),
				match[0].major,match[1].major, match[2].major,
				inv_map[match[0].time_zone],inv_map[match[1].time_zone], inv_map[match[2].time_zone],
				match[0].meeting_freq_str,match[1].meeting_freq_str, match[2].meeting_freq_str,
				match[0].partner_type_str,match[1].partner_type_str, match[2].partner_type_str,
				', '.join(match[0].meeting_work_type),', '.join(match[1].meeting_work_type), ', '.join(match[2].meeting_work_type),
				match[0].meeting_times_str,match[1].meeting_times_str, match[2].meeting_times_str,
				match[0].phone,match[1].phone, match[2].phone,
				inv_map_meeting_type[match[0].meeting_type],inv_map_meeting_type[match[1].meeting_type], inv_map_meeting_type[match[2].meeting_type],
				])

	with open(filename, 'w') as csvfile:  
	    # creating a csv writer object  
	    csvwriter = csv.writer(csvfile)  
	        
	    # writing the fields  
	    csvwriter.writerow(fields)  
	        
	    # writing the data rows  
	    csvwriter.writerows(write_matches)



if __name__ == "__main__":
    main()