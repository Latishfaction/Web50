persons = [
	{"name" : "Guddu", "location": "Katol"},
	{"name" : "Kaaleen", "location": "Wardha"},
	{"name" : "Bablu", "location": "Nagpur"},
        {"name" : "Dablu", "location": "Ajni"}
]


persons.sort(key = lambda persons: persons["location"])

print(persons)
