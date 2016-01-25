from subprocess import Popen, PIPE, STDOUT
from PIL import Image
import sys
import StringIO
import random

def check_output_input(*popenargs, **kwargs):
    """Run command with arguments and return its output as a byte string.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    >>> check_output(["ls", "-l", "/dev/null"])
    'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    'ls: non_existent_file: No such file or directory\n'

    There is an additional optional argument, "input", allowing you to
    pass a string to the subprocess's stdin.  If you use this argument
    you may not also use the Popen constructor's "stdin" argument, as
    it too will be used internally.  Example:

    >>> check_output(["sed", "-e", "s/foo/bar/"],
    ...              input=b"when in the course of fooman events\n")
    b'when in the course of barman events\n'

    If universal_newlines=True is passed, the return value will be a
    string rather than bytes.

    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    if 'input' in kwargs:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        inputdata = kwargs['input']
        del kwargs['input']
        kwargs['stdin'] = PIPE
    else:
        inputdata = None
    process = Popen(*popenargs, stdout=PIPE, **kwargs)
    try:
        output, unused_err = process.communicate(inputdata)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, output=output)
    return output

def get_image(organism):
	command = (
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
	return check_output_input(['./a.out'], input=command, stderr=STDOUT)

orig = Image.open("ORIGINAL.png")
orig = orig.convert("RGB")
orig_pix = orig.load()
def check_fitness(organism):
	image = get_image(organism)

	img  = Image.open(StringIO.StringIO(image))

	if img.size != orig.size:
		print("NOT VALID: image dimensions do not match the original")
		exit()

	w, h = img.size

	
	img = img.convert("RGB")
	img_pix = img.load()

	score = 0

	for x in range(w):
		for y in range(h):
			orig_r, orig_g, orig_b = orig_pix[x,y]
			img_r, img_g, img_b = img_pix[x,y]
			score += (img_r-orig_r)**2
			score += (img_g-orig_g)**2
			score += (img_b-orig_b)**2

	return (score/255.**2)

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
		f.write(get_image(current_gen[0]))
