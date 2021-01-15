import pandas as pd
import csv 
import random 
from enum import Enum

import shared

compatability_scores = dict()

def compute_similarity_score(student1, student2):
	score = 0
	
	if student1.major == student2.major:
		score +=0.75
		if student1.role == student2.role:
			score+=0.25
	else:
		if shared.grad_major_types[student1.major] == shared.grad_major_types[student2.major]:
			score += 0.25
			if shared.grad_majors_groups[student1.major] == shared.grad_majors_groups[student2.major]:
				score += 0.25
		if student1.role == student2.role:
			score+=0.15

	if student1.work_type == student2.work_type:
		score+=0.15
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

def assign_last_student(matches,scores,last_student):
	best_score = 0 
	index = 0 
	index_of_assign = 0
	for match in matches:
		score1 = compute_similarity_score(match[0], last_student)
		score2 = compute_similarity_score(match[0], last_student)
		avg_score = (score1 +score2)/2
		if avg_score > best_score
			index_of_assign = index
			best_score = avg_score
		index+=1 
	return index_of_assign

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

	## To prevent people from signing up twice
	## if they sign up twice we take the most up to date version 
	email_to_student = dict()
	for index, student in student_data.iterrows():
		name = student[shared.q_full_name].strip()
		role = student[q_role].strip()
		work_type = student[shared.q_role].strip()
		work_type = shared.type_of_work[work_type]
		email =  student[shared.q_email_address].strip()
		time_zone = student[shared.q_time_zone].strip()
		time_zone = shared.time_zones[time_zone]
		meeting_freq = student[shared.q_meeting_freq].strip()
		meeting_freq = shared.meeting_frequency[meeting_freq]
		meeting_times = student[shared.q_meeting_times].strip().split(',')
		meeting_times = list(map(lambda mt: shared.meeting_times[mt], meeting_times))
		major = student[shared.program].strip()
		newStudent = shared.GradStudent(name = name, year =year, email = email,
			role = role,
			work_type = work_type,
			time_zone = time_zone,
			meeting_freq = meeting_freq,
			meeting_times = meeting_times,
			major = major)
		email_to_student[email] = newStudent
	best_score = float('inf') 
	students = list(email_to_student.values())
	
	## FIRST ROUND
	compatability_scores = calculate_all_scores(students)
	matches = random_assign(students )
	current_score = get_current_score(matches,compatability_scores)
	num_rounds = 100 
	num_students = len(students)
	for i in range(num_rounds):
		for j in range(len(students)):
			matches, last_student = random_assign(students )
		current_score = get_current_score(matches, compatability_scores)
	print('Current overall_score: ' + str(current_score))

	## NEXT ROUNDS 
	num_initialize = 1000
	best_matches = matches
	best_score = current_score
	for i in range(num_initialize):
		matches, last_student = random_assign(students )
		current_score = get_current_score(matches,compatability_scores)
		num_rounds = 100 
		num_students = len(students)
		for i in range(num_rounds):
			for j in range(len(students)):
				matches = random_change(matches, compatability_scores)
			current_score = get_current_score(matches, compatability_scores)
		if current_score > best_score:
			best_matches = matches
			best_score = current_score
		print('Current best: ' + str(best_score))
	
	filename = "graduate-matches.csv"
	fields = ['Student 1', 'Student 2','Student 3', 'Student 1 Email', 'Student 2 Email','Student 3 Email']
	index_of_assign = assign_last_student(matches,scores,last_student)
	matches[index_of_assign].append(last_student)
	write_matches = []
	for match in matches:
		if len(match) == 2:
			write_matches.append([match[0].name,match[1].name,' ' ,match[0].email,match[1].email, ' '])
		else:
			write_matches.append([match[0].name,match[1].name,match[2].name ,match[0].email,match[1].email, match[2].email])

	with open(filename, 'w') as csvfile:  
	    # creating a csv writer object  
	    csvwriter = csv.writer(csvfile)  
	        
	    # writing the fields  
	    csvwriter.writerow(fields)  
	        
	    # writing the data rows  
	    csvwriter.writerows(write_matches)

if __name__ == "__main__":
    main()