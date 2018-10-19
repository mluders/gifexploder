import sys
import os
import uuid
from shutil import copyfile
import time

def uuid_path(base_path='./text/', ext='txt'):
	return base_path + str(uuid.uuid4()) + '.' + ext

def load_variants_from_file(path):
	with open(path) as f:
		lines = f.readlines()

	lines = [x.rstrip() for x in lines] # strip new lines
	lines = [x for x in lines if x] # remove blank characters

	return lines


def load_variants_from_output_directory(path):
	files = os.listdir(path) # get a list of files
	names = []

	for f in files:
		segments = f.split('.')
		if len(segments) != 3:
			print('Ignoring ' + f) 
			continue

		names.append(segments[1])

	return names


def get_remaining_variants(variant_path, output_path):
	expected = set(load_variants_from_file(variant_path))
	actual = set(load_variants_from_output_directory(output_path))

	return list(expected-actual)


def create_variant_list_path(comp_name, variant, ext, base_path='./text/'):
	return base_path + '.'.join([comp_name, variant, ext])


def write_variants_to_file(variants, path):
	os.makedirs(os.path.dirname(path), exist_ok=True)

	with open(path, 'w+') as f:
		for v in variants:
			f.write("%s\n" % v)


def copy_jsx(dst, src='./namester.jsx'):
	os.makedirs(os.path.dirname(dst), exist_ok=True)
	copyfile(src, dst)


def replace_in_file(path, replacements):
	with open(path, 'r') as f:
		data = f.read()
	
	for key, value in replacements.items():
		data = data.replace(key, value)
	
	with open(path, 'w') as f:
		f.write(data)


def main():
	if sys.version_info[0] < 3:
		raise Exception('Must be using Python 3 or later')

	if len(sys.argv) != 5:
		raise Exception('Wrong number of arguments')
	
	project_path = sys.argv[1]
	comp_name    = sys.argv[2]
	variant_list_path   = sys.argv[3]
	output_path  = sys.argv[4]

	temp_variant_list_path = uuid_path()
	jsx_path = uuid_path('./jsx/', 'jsx')

	try:
		remaining = get_remaining_variants(variant_list_path, output_path)
		write_variants_to_file(remaining, temp_variant_list_path)

		print('Generating JSX file... ', end='', flush=True)
		
		copy_jsx(jsx_path)
		replace_in_file(jsx_path, {
			'$VARIANT_LIST_PATH$': temp_variant_list_path
		})
		print('Done')

		print('Initiating After Effects render... ', end='', flush=True)
		time.sleep(1)
		# fork after effects process
		# wait for after effects to close
		print('Done')
		
	except Exception as e:
		print(e)
	finally:
		os.remove(temp_variant_list_path)
		#os.remove(jsx_path)


main()
