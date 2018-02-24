import os, errno
import shutil

def Raw_Input(t = ""):
	text_in = raw_input(t)
	if text_in == 'q':
		print("Bye Bye")
		quit()
	else:
		return text_in

def create_dir(directory, replace_old = True):
	if not os.path.exists(directory):
		os.makedirs(directory)
	elif replace_old:
		shutil.rmtree(directory)
		os.makedirs(directory)