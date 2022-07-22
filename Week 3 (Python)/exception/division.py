import sys

try : 
    x = int(input("X : "))
    y = int(input("Y : "))

except ValueError : 
    print("Please enter valid integer")
    sys.exit(1) # status code {error}

try : 
    result = x / y


#except ZeroDivisionError :
#    print("you can't divide by 0, It is invalid")
#    sys.exit(1) # status code {error}

except Exception :
    print("Error Occured,try again.")
    sys.exit(1) # status code {error}

print(result)