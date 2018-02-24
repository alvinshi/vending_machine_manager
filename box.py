class Box:
	def __init__(self, name, unit_cost, numerator, denominator):
		self.name = name
		self.unit_cost = unit_cost
		self.numerator = numerator
		self.denominator = denominator

	def __str__(self):
		return self.name