'''
✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈
                    
                    Flight Booking Mechanism with class

    Things to consider:
    > capacity : capacity of a flight
    > Availability : must check , if the flight available or not
    > passenger : accepts name of a passenger
 
✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈
'''
class Flight():
    def __init__(self,capacity):
        self.capacity = capacity
        self.passenger = []  #adding list for storing list of all passenger (for later purpose)

    def addPassenger(self,name): # taking name of a passenger
        def isAvailable(self):
        # total capacity - length of total passenger
            return self.capacity - len(self.passenger)

            
        # if isAvailable() == 0 || isAvailable() <= 0 
        if not isAvailable(self): 
            return False #failure status code
        self.passenger.append(name) #adding passenger name to the lists
        return True  # success status code
    

PrivateJet = Flight(4) 

passengers = ["Latish","Guddu","Bablu","Loki","Tony","Peter"]

print("✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈")

for person in passengers:
    status = PrivateJet.addPassenger(person)

    if status:
        print(f"{person} flight booked successfully ✔")
    else:
        print(f"Sorry {person}, no flights available ☹")


print("✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈✈")
