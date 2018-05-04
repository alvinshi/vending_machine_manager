class Box:
	def __init__(self, box_index, name, unit_cost, numerator, denominator):
		self.box_index = box_index
		self.name = name
		self.unit_cost = unit_cost
		self.numerator = numerator
		self.denominator = denominator

	def __str__(self):
		return self.name