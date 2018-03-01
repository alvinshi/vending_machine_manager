################################################
############### VMM Version 1.2 ################
################################################

import helper as h
from manual_input_mode import manual_input_mode
from csv_import_mode import csv_import_mode

mode_dict = {1: manual_input_mode, 2: csv_import_mode}

def welcome():
	h.print_title("WELCOME TO VMM VERSION 1.0")
	print("Please select the input mode you would like to use")
	print("1 for manual input mode, 2 for csv import mode")
	text_in = ''
	while (text_in != 'q'):
		text_in = h.Raw_Input("Please enter the corresponding number: ")
		try:
			mode = int(text_in)
			if (mode_dict.has_key(mode)):
				return mode
			print("Invalid mode entered")
		except:
			print("Invalid mode entered")

def main():
	mode = welcome()
	func = mode_dict[mode]
	func()

main()