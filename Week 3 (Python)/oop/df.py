class Flight():
	def __init__(self, capacity):
		self.capacity = capacity
		self.passenger = []
	
	def add_passenger(self,name):
		if IsAvailable ==0:
			return False
		self.passenger.append(name)
		return True

		def IsAvailable(self):
			return self.capacity - len(self.passenger)
	


AirIndia = Flight(3)

person = ["Guddu","Bablu","Kaleen","Sweety"]

for people in person:
	status = AirIndia.add_passenger(people)
	if status:
		print(f" {people} Flight Booked Successfully")
	else :
		print(f" Sorry {people} , flight is full currently.")