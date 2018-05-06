# This is a wrapper for the worksheet object provided by xlsxwriter
class Worksheet:

	def col_to_a(self, column):
		return chr(ord('A') + column)

	def __init__(self, worksheet):
		self.worksheet = worksheet
		self.next_row = 1
		self.last_col_count = {}
		self.SUMMARY_START_ROW = 102

	def write(self, args):
		for index, value in enumerate(args):
			cell = "%c%d" % (self.col_to_a(index), self.next_row)
			self.worksheet[cell] = value
		self.last_col_count[self.next_row] = len(args) - 1
		self.next_row += 1

	def write_summary(self, summary_dict):
		row = self.SUMMARY_START_ROW
		for key,value in summary_dict.iteritems():
			index = 0
			cell = "%c%d" % (self.col_to_a(index), row)
			self.worksheet[cell] = ""
			index+=1
			cell = "%c%d" % (self.col_to_a(index), row)
			self.worksheet[cell] = ""
			index+=1
			cell = "%c%d" % (self.col_to_a(index), row)
			self.worksheet[cell] = key
			index+=1
			cell = "%c%d" % (self.col_to_a(index), row)
			self.worksheet[cell] = value
			row+=1


	def delete_row(self, num = 1):
		while (num >= 1) and (self.next_row > 1):
			for i in xrange(self.last_col_count[self.next_row - 1] + 1):
				cell = "%c%d" % (self.col_to_a(i), self.next_row - 1)
				self.worksheet[cell] = ""
			num -= 1
			self.next_row -= 1

	def replace(self, worksheet):
		self.worksheet = worksheet
