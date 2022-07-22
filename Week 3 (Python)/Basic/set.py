#initializing {set}
s = set()

#adding elements in a set

s.add(1);
s.add(2);
s.add(3);
s.add(4);
s.add(5);

# set do not accept repeated elements
s.add(1)

print(s)
# removing elements
s.remove(2)

print("----- After removing Values -----")
print(s)