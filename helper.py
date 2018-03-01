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

def print_title(title):
	TITLE_LENGTH = 100;
	print
	print("*" * TITLE_LENGTH)
	print("*" * TITLE_LENGTH)
	half_len = (TITLE_LENGTH - len(title) - 4) / 2
	print "*" * half_len,
	print " %s " % title,
	print "*" * half_len
	print("*" * TITLE_LENGTH)
	print("*" * TITLE_LENGTH)
	print

def print_sub_title(title):
	TITLE_LENGTH = 100;
	offset = (len(title) % 2 == 0) if 0 else 1
	print
	print("*" * TITLE_LENGTH)
	half_len = (TITLE_LENGTH - len(title) - 4) / 2
	print "*" * half_len,
	print " %s " % title,
	print "*" * (half_len + offset)
	print("*" * TITLE_LENGTH)
	print
