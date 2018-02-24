from box import Box

class Shipment:
	def __init__(self, index, capacity=100, cost_threshold=200):
		self.index = index
		self.capacity = capacity
		self.boxes = []
		self.total_cost = 0
		self.cost_threshold = cost_threshold
		self.threshold_reached = False

	def add(self, box):
		# Check Invalid Input
		if (not isinstance(box, Box)):
			return False
		elif (len(self.boxes) == self.capacity):
			return False
		elif (box.unit_cost >= self.cost_threshold) and self.threshold_reached:
			return False

		# Insert the Box into this shipment
		self.total_cost += box.unit_cost
		self.boxes.append(box)
		if box.unit_cost >= self.cost_threshold:
			self.threshold_reached = True
		return True

	def remove_recent(self, box, amount):
		for i in xrange(amount):
			poped_box = self.boxes.pop()
			assert(poped_box.name == box.name)
			self.total_cost -= poped_box.unit_cost
			if poped_box.unit_cost >= self.cost_threshold:
				self.threshold_reached = False

	def __str__(self):
		return "Shipment %d" % (self.index + 1)
