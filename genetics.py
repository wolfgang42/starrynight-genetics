import random
import genetics_lib

def get_image_command(organism):
	return (
		chr(len(organism['squares'])+1) +
		''.join([chr(organism['bg'][c]) for c in ['r', 'g', 'b']]) +
		chr(0) + chr(193) + chr(0) + chr(160) +
		''.join([
			''.join([chr(s['colour'][c]) for c in ['r', 'g', 'b']])+
			''.join([
				chr(s[x])
				for x in ['xs', 'xe', 'ys', 'ye']
			])
			for s in organism['squares']
		])
	)


def check_fitness(organism):
	if 'fitness' in organism:
		# Fitness already calculated; don't bother doing it again
		# IMPORTANT: This depends on mutations returning a copy!
		return organism['fitness']

	image = get_image_command(organism)
	fitness=genetics_lib.check_fitness(image)
	organism['fitness'] = fitness
	return fitness

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

def clamp_colour(c):
	for colour in ['r','g','b']:
		c[colour] = clamp(c[colour], 0, 255)

def random_colour():
	return {
		'r': random.randint(0, 255),
		'g': random.randint(0, 255),
		'b': random.randint(0, 255),
	}

def mutate_colour(old_colour):
	return {
		'r': clamp(old_colour['r']+random.randint(-10, 10), 0, 255),
		'g': clamp(old_colour['g']+random.randint(-10, 10), 0, 255),
		'b': clamp(old_colour['b']+random.randint(-10, 10), 0, 255),
	}

def clamp_square(s):
	clamp_colour(s['colour'])
	s['xs'] = clamp(s['xs'], 0, 193)
	s['xe'] = clamp(s['xe'], 0, 193)
	s['ys'] = clamp(s['ys'], 0, 160)
	s['ye'] = clamp(s['ye'], 0, 160)
	if s['xe'] < s['xs']:
		s['xe'], s['xs'] = s['xs'], s['xe']
	if s['ye'] < s['ys']:
		s['ye'], s['ys'] = s['ys'], s['ye']
	return s

def random_square(UNUSED_ARG):
	return clamp_square({
		'colour': random_colour(),
		'xs': random.randint(0, 193),
		'xe': random.randint(0, 193),
		'ys': random.randint(0, 160),
		'ye': random.randint(0, 160),
	})

def mutate_squares(old_squares):
	new_squares = list(old_squares) # Copy array, to avoid mutating it
	if random.randint(0, 100) == 0:
		new_squares.append(random_square())
	if random.randint(0, 100) == 0:
		new_squares = random.sample(new_squares, len(old_squares)-1)
	# TODO change some squares

def mutate(orig):
	new = {'squares': orig['squares'], 'bg': mutate_colour(orig['bg'])}
	return new

def sort_by_fitness(generation):
	generation.sort(key=check_fitness)

def random_organism():
	return {
		'bg': random_colour(),
		'squares':map(random_square, [0]*random.randint(0, 4))
	}

def new_generation(old_gen):
	new_gen = (
		old_gen # Keep the old generation to compare against
		+ map(mutate, random.sample(old_gen, len(old_gen)/2)) # Make some mutations
		+ [random_organism()] # Also generate a completely random one
	)
	sort_by_fitness(new_gen)
	return new_gen[0:len(old_gen)]

current_gen = (
	[random_organism() for g in range(9)]
	+[
		{
			'name': 'AA',
			'bg': {'r': 94, 'g': 94, 'b': 94},
			'squares': [
				{'colour': {'r': 223, 'b': 92, 'g': 40}, 'ye': 100, 'xe': 100, 'xs': 51, 'ys': 42},
				{'colour': {'r': 187, 'b': 41, 'g': 232}, 'ye': 47, 'xe': 168, 'xs': 127, 'ys': 22},
				{'colour': {'r': 45, 'b': 119, 'g': 223}, 'ye': 92, 'xe': 32, 'xs': 29, 'ys': 71}
			]
		},
		{
			'name': 'BB',
			'bg': {'r': 99, 'g': 99, 'b': 99},
			'squares': [
				{'colour': {'r': 106, 'b': 229, 'g': 7}, 'ye': 115, 'xe': 32, 'xs': 6, 'ys': 52}
			]
		},
		{
			'name': 'CC',
			'bg': {'r': 92, 'g': 92, 'b': 92},
			'squares': [
				{'colour': {'r': 111, 'b': 152, 'g': 122}, 'ye': 16, 'xe': 111, 'xs': 26, 'ys': 13}
			]
		},
		{
			'name': 'DD',
			'bg': {'r': 92, 'g': 92, 'b': 92},
			'squares': []
		},
		{
			'name': 'EE',
			'bg': {'r': 78, 'b': 107, 'g': 93},
			'squares': []
		},
	]
)
for i in range(20):
	current_gen = new_generation(current_gen)
	print current_gen
	print
	with open('result-'+str(i)+'.ppm', 'w') as f:
		f.write(genetics_lib.get_image(get_image_command(current_gen[0])))
