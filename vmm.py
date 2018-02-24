import os, errno
import random

import xlsxwriter
from worksheet import Worksheet
import helper as h
from shipment import Shipment
from box import Box

OUPTPUT_FOLDER_PATH = "output"
SHIPMENTS = 200


def manual_input_mode():
	required_args = 3
	is_full = False

	def input_parse(t):
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
			# if shipments % denominator != 0:
			# 	print("Invalid Input: Ns must be a divider of %d" % SHIPMENTS)
			# 	return None
		except TypeError:
			print("Invalid Input: %s"% t)
			return None
		return (name, unit_cost, numerator, denominator)

	def init():
		# Initialize the output directory
		h.create_dir(OUPTPUT_FOLDER_PATH)

		# Initializie the workbook
		workbook = xlsxwriter.Workbook(OUPTPUT_FOLDER_PATH + '/shipments.xlsx')
		worksheets = []
		shipments = []
		for i in xrange(SHIPMENTS):
			worksheets.append(Worksheet(workbook.add_worksheet("Shipment%d" % (i + 1))))
			shipments.append(Shipment(i))
		return (workbook, worksheets, shipments)

	def reopen(wrapped_worksheets):
		workbook = xlsxwriter.Workbook(OUPTPUT_FOLDER_PATH + '/shipments.xlsx')
		worksheets = workbook.worksheets()
		for index, worksheet in enumerate(worksheets):
			wrapped_worksheets[index].replace(worksheet)
		return workbook


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
			while (not assigned):
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
		print_allocation_result(allocation_results)



	print("MANUAL INPUT MODE")
	(workbook, worksheets, shipments) = init()

	while (not is_full):
		print("Please enter '<Product_Name> <Product_Price> <N/Ns>': ")
		text_in = h.Raw_Input()
		parsed = input_parse(text_in)
		if (parsed):
			name, unit_cost, numerator, denominator = parsed

			# Create new_boxes
			new_boxes = []
			for i in xrange(SHIPMENTS / denominator * numerator):
				new_boxes.append(Box(name, unit_cost, numerator, denominator))

			# Allocate new_boxes
			allocate_boxes(new_boxes, shipments, worksheets)

			# This is a very inefficient processs
			# However, this is done so that the user can see changes in the xlsx sheet in real time
			workbook.close()
			workbook = reopen(worksheets)

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