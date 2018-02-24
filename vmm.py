import os, errno
import random
import openpyxl
from openpyxl import Workbook

from worksheet import Worksheet
import helper as h
from shipment import Shipment
from box import Box

OUPTPUT_FOLDER_PATH = "output"
SHIPMENTS = 200
TRY_THRESHOLD = 50
CAPACITY = 100


def manual_input_mode():
	required_args = 3
	is_full = False

	def input_parse(t):
		if t == "backtrack":
			return ("backtrack", 0, 0, 0)
		elif t == "generate_report":
			return ("generate_report", 0, 0, 0)

		l_in = t.split()
		if (len(l_in) != required_args):
			print("Invalid Input: Please input three parameters with the descripted format")
			return None
		name = l_in[0].decode('utf-8')
		try:
			unit_cost = float(l_in[1])
			numerator, denominator = l_in[2].split("/")
			numerator = int(numerator)
			denominator = int(denominator)
			if SHIPMENTS % denominator != 0:
				print("Invalid Input: Ns must be a divider of %d" % SHIPMENTS)
				return None
		except TypeError:
			print("Invalid Input: %s"% t)
			return None
		return (name, unit_cost, numerator, denominator)

	def init():
		# Initialize the output directory
		h.create_dir(OUPTPUT_FOLDER_PATH)

		# Initializie the workbook
		workbook = Workbook(write_only=False)
		worksheets = []
		shipments = []
		for i in xrange(SHIPMENTS):
			worksheets.append(Worksheet(workbook.create_sheet("Shipment%d" % (i + 1), i)))
			shipments.append(Shipment(i))
		return (workbook, worksheets, shipments)

	def print_allocation_result(allocation_results):
		print("Allocation Result:")
		for key, value in allocation_results.iteritems():
			print("%s : %d" % (str(key), value))

	def allocate_boxes(new_boxes, shipments, worksheets):
		assert(len(shipments) == len(worksheets))
		assert(len(shipments) == SHIPMENTS)
		allocation_results = {}
		for new_box in new_boxes:
			assigned = False
			count = 0
			while (not assigned) and (count < TRY_THRESHOLD):
				count += 1
				index = random.randint(0, SHIPMENTS - 1)
				shipment = shipments[index]
				assigned = shipment.add(new_box)
				if assigned:
					if not shipment in allocation_results:
						allocation_results[shipment] = 1
					else:
						allocation_results[shipment] = allocation_results[shipment] + 1
					index = shipment.index
					args = [new_box.name, new_box.unit_cost]
					worksheets[index].write(args)
		if (count == TRY_THRESHOLD):
			return (None, allocation_results, 
				"Too many items in the box, please try to assign the item manually, an error may exist")
		print_allocation_result(allocation_results)
		workbook.save(OUPTPUT_FOLDER_PATH + '/shipments.xlsx')
		return (new_boxes[0], allocation_results, "")

	def backtrack(new_box, allocation_results, shipments, worksheets):
		assert(len(shipments) == len(worksheets))
		assert(len(shipments) == SHIPMENTS)
		if (new_box == None): return
		for shipment, amount in allocation_results.iteritems():
			shipment.remove_recent(new_box, amount)
			worksheets[shipment.index].delete_row(amount)
		workbook.save(OUPTPUT_FOLDER_PATH + '/shipments.xlsx')

	def generate_report(shipments):
		f = open(OUPTPUT_FOLDER_PATH+"/report.txt", "w+")
		for index, shipment in enumerate(shipments):
			f.write("Shipment %d :\n" % (index + 1))
			length = len(shipment.boxes)
			f.write("  Total Boxes: %d\n" % length)
			f.write("  Total Cost:  {:.2f}\n".format(shipment.total_cost))
			if (length > 0):
				f.write("  Average Cost:  {:.2f}\n".format(shipment.total_cost / len(shipment.boxes)))
				f.write("  Has Big Price: %r\n" % shipment.threshold_reached)
		f.close()

	print("MANUAL INPUT MODE")
	(workbook, worksheets, shipments) = init()

	# Start to take in inputs
	new_box = None
	allocation_results = {}
	total_boxes = 0
	while (total_boxes < SHIPMENTS * CAPACITY):
		print("Please enter '<Product_Name> <Product_Price> <N/Ns>' or 'backtrack' or 'generate_report' or 'q': ")
		text_in = h.Raw_Input()
		parsed = input_parse(text_in)
		if (parsed):
			name, unit_cost, numerator, denominator = parsed
			if name == 'backtrack':
				backtrack(new_box, allocation_results, shipments, worksheets)
			elif name == 'generate_report':
				generate_report(shipments)
			else:
				# Create new_boxes
				new_boxes = []
				for i in xrange(SHIPMENTS / denominator * numerator):
					new_boxes.append(Box(name, unit_cost, numerator, denominator))

				# Allocate new_boxes
				(new_box, allocation_results, error) = allocate_boxes(new_boxes, shipments, worksheets)
				if (new_box == None):
					print(error)
					quit()
				total_boxes += SHIPMENTS / denominator * numerator

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