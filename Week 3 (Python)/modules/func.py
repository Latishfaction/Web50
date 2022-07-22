# imports whole method in square.py file
# import square as sq    or


# imports only one method from square.py file

from square import square
for i in range(10):
    print(f"Square of {i} is {square(i)}")