import box

class Shipment:
	def __init__(self, capacity=100):
		self.capacity = capacity
		self.boxes = []
		self.total_cost = 0

	def add(box):
		if (not isinstance(o, Box)):
			return False
		elif (len.boxes == self.capacity):
			return False

		self.total_cost += box.unit_cost
		self.boxes.append(box)
		return True
