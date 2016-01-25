from random import randint, choice, random
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


def command_colour(c):
	if len(c) != 3: raise ValueError("Invalid colour passed")
	return chr(c[0])+chr(c[1])+chr(c[2])
def command_range(r):
	if len(r) != 2: raise ValueError("Invalid range passed")
	return chr(r[0])+chr(r[1])
def command_coords(c):
	if c[0][1] > 193: raise ValueError("X coordinate too large")
	if c[1][1] > 160: raise ValueError("Y coordinate too large: "+str(r[1]))
	return command_range(c[0]) + command_range(c[1])
def command_shape(s):
	ret = command_colour(s[1]) + command_coords(s[0])
	if len(ret) != 7: raise ValueError("Unexpected shape arrangement")
	return ret
def command_organism(organism):
	return (
		chr(111) + # All organisms have exactly 110 shapes, plus the background
		command_shape((((0, 193), (0, 160)), organism[0])) +
		''.join([command_shape(organism[1][s]) for s in range(110)])
	)

def mate_int(parent1, parent2, maximum):
	r = random()
	movement = 0
	if randint(0, 50) == 0:
		movement = randint(-50, 50)
	return int(clamp(
		parent1*r + parent2*(1-r) + movement,
		0, maximum
	))

def mate_colours(parent1, parent2):
	# TODO mutations
	return (
		mate_int(parent1[0], parent2[0], 255),
		mate_int(parent1[1], parent2[1], 255),
		mate_int(parent1[2], parent2[2], 255),
	)

def mate_range(parent1, parent2, maximum):
	# TODO mutations
	return ordered_pair((
		mate_int(parent1[0], parent2[0], maximum),
		mate_int(parent1[1], parent2[1], maximum),
	))

def mate_coords(parent1, parent2):
	# TODO mutations
	return (
		mate_range(parent1[0], parent2[0], 193),
		mate_range(parent1[1], parent2[1], 160),
	)

def mate_shape(parent1, parent2):
	# TODO mutations
	return (
		mate_coords(parent1[0], parent2[0]),
		mate_colours(parent1[1], parent2[1])
	)

def mate_organism(parent1, parent2):
	# TODO mutations
	shapes = [mate_shape(parent1[1][x], parent2[1][x]) for x in range(110)]
	for i in range(randint(0, 10)):
		n1 = randint(0, 109)
		n2 = randint(0, 109)
		shapes[n1], shapes[n2] = shapes[n2], shapes[n1]
	return (
		mate_colours(parent1[0], parent2[0]),
		tuple(shapes)
	)

def new_generation(old_gen):
	new_gen = list(old_gen)
	for i in range(len(old_gen)):
		new_gen.append(mate_organism(choice(old_gen), choice(old_gen)))
	new_gen.sort(key=lambda o: genetics_lib.check_fitness(command_organism(o)))
	return tuple(new_gen[0:len(old_gen)])

current_gen = tuple([random_organism() for x in range(20)])
for i in range(20):
	current_gen = new_generation(current_gen)
	#pprint(current_gen)
	with open('result-'+str(i)+'.ppm', 'w') as f:
		f.write(genetics_lib.get_image(command_organism(current_gen[0])))
