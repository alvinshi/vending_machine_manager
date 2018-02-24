import xlsxwriter

# This is a wrapper for the worksheet object provided by xlsxwriter
class Worksheet:
	def __init__(self, worksheet):
		self.worksheet = worksheet
		self.next_row = 0
		self.last_col_count = {}

	def write(self, args):
		for index, value in enumerate(args):
			self.worksheet.write(self.next_row, index, value)
		self.last_col_count[self.next_row] = len(args) - 1
		self.next_row += 1

	def delete_row(self, num = 1):
		while (num >= 1) and (self.next_row > 0):
			for i in xrange(self.last_col_count[self.next_row - 1] + 1):
				self.worksheet.write(self.next_row - 1, i, None)
			num -= 1
			self.next_row -= 1

	def replace(self, worksheet):
		self.worksheet = worksheet
