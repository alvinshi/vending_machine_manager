def Raw_Input(t = ""):
	text_in = raw_input(t)
	if text_in == 'q':
		print("Bye Bye")
		quit()
	else:
		return text_in