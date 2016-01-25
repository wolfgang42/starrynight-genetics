from random import randint
from pprint import pprint
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

def new_generation(old_gen):
	new_gen = list(old_gen)
	new_gen.sort(key=lambda o: genetics_lib.check_fitness(command_organism(o)))
	return tuple(new_gen)

current_gen = tuple([random_organism() for x in range(20)])
current_gen = new_generation(current_gen)
pprint(current_gen)
with open('result.ppm', 'w') as f:
	f.write(genetics_lib.get_image(command_organism(current_gen[0])))
