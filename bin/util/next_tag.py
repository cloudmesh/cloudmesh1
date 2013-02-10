from sh import cat
from sh import echo

filename = "VERSION.txt"

print cat(filename)

numbers = cat(filename).split(".")

numbers[-1] = str(int(numbers[-1]) + 1)
version = ".".join(numbers)


file = open (filename, 'w')
print >> file, version
file.close()

print "New Version Number:"
print cat(filename)
