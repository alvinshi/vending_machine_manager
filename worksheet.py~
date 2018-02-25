import xlsxwriter

# This is a wrapper for the worksheet object provided by xlsxwriter
class Worksheet:
	def col_to_a(self, column):
		return chr(ord('A') + column)

	def __init__(self, worksheet):
		self.worksheet = worksheet
		self.next_row = 1
		self.last_col_count = {}

	def write(self, args):
		for index, value in enumerate(args):
			cell = "%c%d" % (self.col_to_a(index), self.next_row)
			print(cell)
			self.worksheet[cell] = value
		self.last_col_count[self.next_row] = len(args) - 1
		self.next_row += 1

	def delete_row(self, num = 1):
		while (num >= 1) and (self.next_row > 1):
			for i in xrange(self.last_col_count[self.next_row - 1] + 1):
				cell = "%c%d" % (self.col_to_a(i), self.next_row - 1)
				self.worksheet[cell] = ""
			num -= 1
			self.next_row -= 1
			print(self.next_row)

	def replace(self, worksheet):
		self.worksheet = worksheet
