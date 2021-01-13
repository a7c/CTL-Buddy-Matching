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

meeting_times = {
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
	'Civil and Environmental Engineering': 1,
	'Classics': 4, 
	'Communication': 4, 
	'Community Health and Prevention Research': 2, 
	'Comparative Literature': 4, 
	'Comparative Studies in Race and Ethnicity': 4, 
	'Computer Science' : 1,
	'Democracy, Development, and the Rule of Law': 3, 
	'Earth Systems': 2, 
	'East Asian Studies': 3,
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
	'Jewish Studies': 3, 
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

# strings for question prompts
q_full_name = 'Full Name'
q_year = 'Year'
q_email_address = 'Email Address'
q_time_zone = 'Time Zone (time zone where you will be located during Winter quarter)'
q_meeting_freq = 'How often do you wish to meet?'
q_meeting_times = 'Preferred Meeting Time(s)'
q_classes = 'Please select (up to four) courses for which you would want an accountability partner.'
q_major = 'Major'