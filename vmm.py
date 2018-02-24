import helper as h
import shipment
import box

def manual_input_mode():
	required_args = 3
	is_full = False

	def input_parse(t):
		l_in = t.split()
		if (len(l_in) != required_args):
			print("Invalid Input: %s"% t)
			return None
		name = l_in[0].decode('utf-8')
		try:
			unit_cost = float(l_in[1])
			numerator, denominator = l_in[2].split("/")
			numerator = int(numerator)
			denominator = int(denominator)
		except TypeError:
			print("Invalid Input: %s"% t)
			return None
		return (name, unit_cost, numerator, denominator)	

	print("MANUAL INPUT MODE")
	while (not is_full):
		print("Please enter '<Product_Name> <Product_Price> <N/Ns>': ")
		text_in = h.Raw_Input()
		parsed = input_parse(text_in)
		if (parsed):
			name, unit_cost, numerator, denominator = parsed
			new_box = box.Box(name, unit_cost, numerator, denominator)

def csv_import_mode():
	print("CSV IMPORT MODE")
	print("WARNING: The current version does not support CSV Import Mode, exiting...")

mode_dict = {1: manual_input_mode, 2: csv_import_mode}

def welcome():
	print("WELCOME TO VMM VERSION 1.0")
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