class Student:
	def __init__(self, name, year, on_campus, time_zone, meeting_freq, meeting_time, classes, major):
		self.name = name
		self.year = year
		self.on_campus = on_campus
		self.time_zone = time_zone
		self.meeting_freq = meeting_freq
		self.meeting_time = meeting_time
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
	'Evening 16:00-20:00': 18,
	'Night 20:00-24:00': 22,
}