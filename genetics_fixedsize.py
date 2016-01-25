from random import randint
import genetics_lib

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def ordered_pair(p):
	if p[0] > p[1]:
		return (p[1], p[0])
	else:
		return (p[0], p[1])

def random_colour():
	return (randint(0,255), randint(0,255), randint(0,255))

def random_range(maximum):
	return ordered_pair((randint(0, maximum), randint(0, maximum)))

def random_coords():
	return (random_range(193), random_range(160))

def random_shape():
	return (random_coords(), random_colour())

def random_organism():
	return (random_colour(), tuple([random_shape() for x in range(110)]))


def command_base(c):
	return ''.join([chr(x) for x in c])
def command_coords(c):
	return command_base(c[0]) + command_base(c[1])
def command_shape(s):
	return command_coords(s[0]) + command_base(s[1])
def command_organism(organism):
	return (
		chr(110) + # All organisms have exactly 110 shapes
		command_base(organism[0]) +
		''.join([command_shape(s) for s in organism[1]])
	)

for i in range(10):
	with open('fixed'+str(i)+'.ppm', 'w') as f:
		f.write(genetics_lib.get_image(command_organism(random_organism())))
