from itertools import combinations
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
RANDOM_MODE = 1
PARTIAL_RANDOM_MODE = 2
NON_RANDOM_MODE = 3
COST_THRESHOLD = 200

def n_random_in_l(l, n):
	assert(len(l) > n)
	random.shuffle(l)
	return l[0:n]


def read_mode(str):
	mode = NON_RANDOM_MODE
	if (str == "RAND"):
		mode = RANDOM_MODE
	elif (str == "P_RAND"):
		mode = PARTIAL_RANDOM_MODE
	elif (str == "N_RAND"):
		mode = NON_RANDOM_MODE
	return mode

def input_parse(t):
	required_args = 4
	if t == "backtrack":
		return ("backtrack", 0, 0, 0, 0)
	elif t == "generate_report":
		return ("generate_report", 0, 0, 0, 0)

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
		allocation_mode = read_mode(l_in[3])

			# Input number validation
		if SHIPMENTS % denominator != 0:
			print("Invalid Input: Ns must be a divider of %d" % SHIPMENTS)
			return None
		if (allocation_mode == NON_RANDOM_MODE) and \
		((numerator < denominator) or (numerator % denominator != 0)):
			print("Invalid Input: In non-random mode, \
				N must larger or equal Ns and Ns must be a divisor or N")
			return None
		if (unit_cost >= COST_THRESHOLD) and (allocation_mode != RANDOM_MODE):
			print("Invalid Input: Please use random mode to allocate big prize")
			return None

	except:
		print("Invalid Input: %s"% t)
		return None
	return (name, unit_cost, numerator, denominator, allocation_mode)

def init():
	# Initialize the output directory
	h.create_dir(OUPTPUT_FOLDER_PATH)

	# Initializie the workbook
	workbook = Workbook(write_only=False)
	worksheets = []
	shipments = []
	for i in xrange(SHIPMENTS):
		worksheets.append(Worksheet(workbook.create_sheet("Shipment%d" % (i + 1), i)))
		shipments.append(Shipment(i, capacity = CAPACITY, cost_threshold = COST_THRESHOLD))
	return (workbook, worksheets, shipments)

def print_allocation_result(allocation_results):
	print("Allocation Result:")
	for key, value in allocation_results.iteritems():
		print("%s : %d" % (str(key), value))

def allocation_results_update(allocation_results, shipment, n):
	if not shipment in allocation_results:
		allocation_results[shipment] = n
	else:
		allocation_results[shipment] = allocation_results[shipment] + n

def worksheet_update(worksheets, index, new_box):
	args = [new_box.name, new_box.unit_cost]
	worksheets[index].write(args)

def non_random_allocation(new_boxes, shipments, worksheets, box_per_shipment, allocation_results):
	new_box_sample = new_boxes[0]
	for shipment in shipments:
		for i in xrange(box_per_shipment):
			new_box = new_boxes.pop()
			assigned = shipment.add(new_box)
			## The box is too full
			if (not assigned):
				return (None, allocation_results, 
					"Shipments are too full for this allocation, please backtrack")

			# Added successfully
			allocation_results_update(allocation_results, shipment, 1)
			worksheet_update(worksheets, shipment.index, new_box)
	return (new_box_sample, allocation_results, "success")

def random_allocation(new_boxes, shipments, worksheets, numerator, denominator, allocation_results):
	new_box_sample = new_boxes[0]
	for new_box in new_boxes:
		assigned = False
		count = 0
		while (not assigned) and (count < TRY_THRESHOLD):
			count += 1
			index = random.randint(0, SHIPMENTS - 1)
			shipment = shipments[index]
			assigned = shipment.add(new_box)
			if assigned:
				allocation_results_update(allocation_results, shipment, 1)
				worksheet_update(worksheets, shipment.index, new_box)
			if (count == TRY_THRESHOLD):
				return (None, allocation_results, 
					"Too many items in the box, please try to assign the item manually, an error may exist")
	return (new_box_sample, allocation_results, "success")

def get_none_full_shipments(shipments):
	rtn = []
	for shipment in shipments:
		if (not shipment.is_full()):
			rtn.append(shipment)
	return rtn

def partial_random_allocation(new_boxes, shipments, worksheets, numerator, denominator, allocation_results):
	assert(len(new_boxes) == SHIPMENTS / denominator * numerator)
	new_box_sample = new_boxes[0]
	if (numerator >= denominator):
		box_per_shipment = numerator / denominator
		numerator = numerator % denominator
		(new_box, allocation_results, msg) = non_random_allocation(new_boxes, shipments, worksheets, box_per_shipment, allocation_results)
		print("non_random_allocation done")
		print(msg)
		if (new_box == None):
			print("failed here")
			return (new_box, allocation_results, msg) # Failed to allocate

	# Start partial_random allocation
	print("passed")
	potential_shipments = get_none_full_shipments(shipments)
	if (len(potential_shipments) < SHIPMENTS / denominator * numerator):
		print(len(potential_shipments))
		print(SHIPMENTS / denominator * numerator)
		print("failed here2")
		return (None, allocation_results, 
			"Shipments are too full for this allocation, please backtrack")

	chosen_shipments_n = SHIPMENTS / denominator * numerator
	chosen_shipments = n_random_in_l(potential_shipments, chosen_shipments_n)
	for shipment in chosen_shipments:
		new_box = new_boxes.pop()
		assigned = shipment.add(new_box)
		assert(assigned)
		allocation_results_update(allocation_results, shipment, 1)
		worksheet_update(worksheets, shipment.index, new_box)
	return (new_box_sample, allocation_results, "success")

def allocate_boxes(new_boxes, shipments, workbook, worksheets, allocation_mode, numerator, denominator):
	assert(len(shipments) == len(worksheets))
	assert(len(shipments) == SHIPMENTS)
	assert(len(shipments) % denominator == 0)

	allocation_results = {}
	result = (None, allocation_results, "Failed")
	# Non random allocation
	if (allocation_mode == NON_RANDOM_MODE):
		result = non_random_allocation(new_boxes, shipments, worksheets, numerator/denominator, allocation_results)
	# Random allocation
	elif (allocation_mode == RANDOM_MODE):
		result = random_allocation(new_boxes, shipments, worksheets, numerator, denominator, allocation_results)
	elif (allocation_mode == PARTIAL_RANDOM_MODE):
		result = partial_random_allocation(new_boxes, shipments, worksheets, numerator, denominator, allocation_results)
	print_allocation_result(allocation_results)
	workbook.save(OUPTPUT_FOLDER_PATH + '/shipments.xlsx')
	return result

def backtrack(new_box, allocation_results, shipments, workbook, worksheets):
	assert(len(shipments) == len(worksheets))
	assert(len(shipments) == SHIPMENTS)
	if (new_box == None): return
	for shipment, amount in allocation_results.iteritems():
		shipment.remove_recent(new_box, amount)
		worksheets[shipment.index].delete_row(amount)
	workbook.save(OUPTPUT_FOLDER_PATH + '/shipments.xlsx')
	# Destroy the allocation_results after backtracking
	allocation_results.clear()

def generate_report(shipments):
	f = open(OUPTPUT_FOLDER_PATH+"/report.txt", "w+")

	# Comparator
	def get_index(shipment):
		return shipment.index

	shipments.sort(key=get_index)
	for shipment in shipments:
		f.write("Shipment %d :\n" % (shipment.index + 1))
		length = len(shipment.boxes)
		f.write("  Total Boxes: %d\n" % length)
		f.write("  Total Cost:  {:.2f}\n".format(shipment.total_cost))
		if (length > 0):
			f.write("  Average Cost:  {:.2f}\n".format(shipment.total_cost / len(shipment.boxes)))
			f.write("  Has Big Price: %r\n" % shipment.threshold_reached)
	f.close()

def manual_input_mode():
	is_full = False

	h.print_sub_title("MANUAL INPUT MODE")
	print("Keywords")
	print("RAND: Random Allocation Mode")
	print("P_RAND: Partially Random Allocation Mode")
	print("N_RAND: None Random Allocation Mode")
	(workbook, worksheets, shipments) = init()

	# Start to take in inputs
	new_box = None
	allocation_results = {}
	total_boxes = 0
	while (total_boxes < SHIPMENTS * CAPACITY):
		print("Please enter '<Product_Name> <Product_Price> <N/Ns> <RAND/P_RAND/N_RAND>' or 'backtrack' or 'generate_report' or 'q': ")
		text_in = h.Raw_Input()
		parsed = input_parse(text_in)
		if (parsed):
			name, unit_cost, numerator, denominator, allocation_mode = parsed
			if name == 'backtrack':
				backtrack(new_box, allocation_results, shipments, workbook, worksheets)
			elif name == 'generate_report':
				generate_report(shipments)
			else:
				# Create new_boxes
				new_boxes = []
				for i in xrange(SHIPMENTS / denominator * numerator):
					new_boxes.append(Box(name, unit_cost, numerator, denominator))

				# Allocate new_boxes
				(new_box, allocation_results, error) = \
				allocate_boxes(new_boxes, shipments, workbook, worksheets, allocation_mode, numerator, denominator)
				if (new_box == None):
					print(error)
					quit()
				total_boxes += SHIPMENTS / denominator * numerator
