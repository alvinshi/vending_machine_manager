from box import Box


class Shipment:
	def __init__(self, index):
		self.index = index # 0-indexing
		self.boxes = []
		self.total_cost = 0.0
		self.prize_threshold_counter = 0
		self.big_prize_threshold_counter = 0

		# Internal Constants
		self.capacity = 100
		self.prize_threshold = 50
		self.big_prize_threshold = 200
		self.prize_limit = 5
		self.big_prize_limit = 1
		

	def add(self, box):
		# Check Invalid Input
		if not self.can_add(box): return False

		# Insert the Box into this shipment
		self.total_cost += box.unit_cost
		self.boxes.append(box)
		if box.unit_cost >= self.prize_threshold:
			self.prize_threshold_counter += 1
		if box.unit_cost >= self.big_prize_threshold:
			self.big_prize_threshold_counter += 1
		return True

	def remove_recent(self, box, amount):
		for i in xrange(amount):
			poped_box = self.boxes.pop()
			assert(poped_box.name == box.name)
			self.total_cost -= poped_box.unit_cost
			if poped_box.unit_cost >= self.big_prize_threshold:
				self.big_prize_threshold_counter -= 1
			if poped_box.unit_cost >= self.prize_threshold:
				self.prize_threshold_counter -= 1

	def is_full(self):
		return self.capacity == len(self.boxes)

	def can_add(self, box):
		if (not isinstance(box, Box)):
			return False
		elif (len(self.boxes) == self.capacity):
			return False
		elif (box.unit_cost >= self.prize_threshold) and \
		(self.prize_threshold_counter == self.prize_limit):
			return False
		elif (box.unit_cost >= self.big_prize_threshold) and \
		(self.big_prize_threshold_counter == self.big_prize_limit):
			return False
		return True

	def __str__(self):
		return "Shipment %d" % (self.index + 1)
