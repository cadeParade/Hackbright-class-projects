from arithmetic import *

while True:
	userinput = raw_input(" >")
	splitaction = userinput.split(" ")
	print splitaction

	if "q" in splitaction:
		print "You will exit."
		exit(0)
	elif splitaction[0] == "+":
		print "You have the correct operator."
		print add(float(splitaction[1]),float(splitaction[2]))
	elif splitaction[0] == "-":
		print "You have the correct operator."
		print subtract(float(splitaction[1]),float(splitaction[2]))
	elif splitaction[0] == "*":
		print "You have the correct operator."
		print multiply(float(splitaction[1]),float(splitaction[2]))
	elif splitaction[0] == "/":
		print "You have the correct operator."
		print divide(float(splitaction[1]),float(splitaction[2]))
	elif splitaction[0] == "square":
		print "You have the correct operator."
		print square(float(splitaction[1]))
	elif splitaction[0] == "cube":
		print "You have the correct operator."
		print cube(float(splitaction[1]))
	elif splitaction[0] == "pow":
		print "You have the correct operator."
		print power(float(splitaction[1]),float(splitaction[2]))
	elif splitaction[0] == "mod":
		print "You have the correct operator."
		print mod(float(splitaction[1]),float(splitaction[2]))
	else:
		print "Please print an operator followed by two integers."




	# place 0 in list identified to be read
	# determine if place 0 is equal to operator
	# if equal, call function for operator
	# if not equal, continue in list of operators until correct operator is determined

#if user inputs q
	#then quit
#el


# while statement - while no q, program runs