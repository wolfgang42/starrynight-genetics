from subprocess import Popen, PIPE, STDOUT, CalledProcessError
from PIL import Image
import StringIO

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

def get_image(command):
	return check_output_input(['./a.out'], input=command, stderr=STDOUT)

orig = Image.open("ORIGINAL.png")
orig = orig.convert("RGB")
orig_pix = orig.load()
def check_fitness(command):
	img  = Image.open(StringIO.StringIO(get_image(command)))

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

	return score/255.**2
