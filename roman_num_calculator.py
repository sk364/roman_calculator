import re
import pygame
import pygbutton
import sys
from pygbutton import *
from pygame.locals import *

calci_scr = pygame.display.set_mode((300,200))

valid_numbers = ["M", "D", "C", "L", "X", "V", "I"]
decimal_numbers = [1000, 500, 100, 50, 10, 5, 1]

number_buttons = []
operator_buttons = []
clear_buttons = []

numbers = []
decimals = []
operators = []

entered_str = ""
err_label = ""
output = ""


# defines the positions and string of all the buttons - numbers and operators
def init_buttons():

	global number_buttons, operator_buttons, clear_buttons

	n1 = pygbutton.PygButton((128,100,44,22), 'M')
	n2 = pygbutton.PygButton((74,100,44,22), 'D')
	n3 = pygbutton.PygButton((20,100,44,22), 'C')
	n4 = pygbutton.PygButton((74,127,44,22), 'L')
	n5 = pygbutton.PygButton((20,127,44,22), 'X')
	n6 = pygbutton.PygButton((74,154,44,22), 'V')
	n7 = pygbutton.PygButton((20,154,44,22), 'I')

	number_buttons = [n1,n2,n3,n4,n5,n6,n7]

	o1 = pygbutton.PygButton((182,100,44,22),'+')
	o2 = pygbutton.PygButton((236,100,44,22),'-')
	o3 = pygbutton.PygButton((182,127,44,22),'*')
	o4 = pygbutton.PygButton((236,127,44,22),'/')
	o5 = pygbutton.PygButton((128,127,44,49),'=')

	operator_buttons = [o1,o2,o3,o4,o5]

	c1 = pygbutton.PygButton((182,154,44,22),'CLR')
	c2 = pygbutton.PygButton((236,154,44,22),'AC')

	clear_buttons = [c1, c2]

def int_to_roman(num):	
	ints = (1000, 900,  500, 400, 100,  90, 50,  40, 10,  9,   5,  4,   1)
   	nums = ('M',  'CM', 'D', 'CD','C', 'XC','L','XL','X','IX','V','IV','I')

	res = ""
	for i in range(len(ints)):
		count = int(num/ints[i])
		res += nums[i] * count
		num -= ints[i] * count

	return res


def roman_to_int(num):
	places = []
	for i in num:
		if not i in valid_numbers:
			return -1

	for i in range(len(num)):
		c = num[i]
		val = decimal_numbers[valid_numbers.index(c)]

		try:
			nextval = decimal_numbers[valid_numbers.index(num[i+1])]
			if nextval>val:	val*=-1

		except IndexError:	pass

		places.append(val)

	s = 0
	for n in places: s+=n

	if int_to_roman(s) == num:
		return s
	else:	return -1


# checking for clicks on number buttons
def number_button_handler(event):
	number_events = []
	for btn in number_buttons:
		number_events += [btn.handleEvent(event)]

	for i in range(7):
		if number_events[i]:
			if 'down' in number_events[i]:	return i

	return -1


# checking for clicks on operator buttons
def operator_button_handler(event):
	operator_events = []
        for btn in operator_buttons:
                operator_events += [btn.handleEvent(event)]

        for i in range(5):
                if operator_events[i]:
                        if 'down' in operator_events[i]:  return i

        return -1


# checking for clicks on clear and all clear buttons		
def clear_button_handler(event):
	clear_events = []
	for btn in clear_buttons:
		clear_events += [btn.handleEvent(event)]

	for i in range(2):
		if clear_events[i]:
			if 'down' in clear_events[i]:	return i

	return -1


def clear_a_key():
	global entered_str
	
	entered_str = entered_str[0:-1]
	print entered_str


def clear_all():
	global entered_str, output

	entered_str = ""
	output = ""


# stores the current string and splits it to store all the roman numerals and operators in different lists
def store_str(s):
	global entered_str,err_label, numbers, operators

	entered_str += s

	numbers = re.sub("[^\w]", " ",  entered_str).split()

	operators = re.sub("[^\W]", " ",entered_str).split()

	for i in numbers:
		if roman_to_int(i) == -1:
			err_label = "Invalid Number"
			entered_str = ""
			break
	for i in operators:
		if len(i)>1:
			err_label = "Invalid Operation"
			entered_str = ""
			break
	if s=='=':
		get_decimals()
		get_output()
		return 0
        else:   return 1


def get_output():
	global output

	length = len(decimals)

	for i in range(length):
		if i!=length-1:
			output += str(decimals[i]) + operators[i]
		else:
			output += str(decimals[i])

	#print str(eval(output))
	if output:
		output = str(int_to_roman(eval(output)))


# function to convert all roman numbers in the input to decimal
def get_decimals():
	global decimals
	#print numbers
	for i in numbers:
		decimals += [roman_to_int(i)]


def draw():
	global output 

	GREY = (170,170,170)
	BLACK = (0,0,0)
	WHITE = (255,255,255)

	calci_scr.fill(GREY)

	# drawing calculator screen panel to show input and output
	pygame.draw.rect(calci_scr, WHITE, ((20,20),(260,60)))

	#drawing roman number buttons
	for btn in number_buttons:
                btn.draw(calci_scr)

	#drawing operator buttons
	for btn in operator_buttons:
		btn.draw(calci_scr)

	# drawing clear and all clear buttons
	for btn in clear_buttons:
                btn.draw(calci_scr)


	# displaying the input string
	font = pygame.font.SysFont(None,30)
        input_lbl = font.render(entered_str,1, (0,0,0))
        calci_scr.blit(input_lbl, (150-(input_lbl.get_rect().width)/2,40))

	#displaying error label, if error
	font2 = pygame.font.SysFont(None,20)
	err_lbl = font2.render(err_label,1,(0,0,0))
	calci_scr.blit(err_lbl, (150-(err_lbl.get_rect().width)/2,80))

	# displaying output
	out_lbl = font.render(output, 1, (0,0,0))
	calci_scr.blit(out_lbl, (150-(out_lbl.get_rect().width)/2,40))
	pygame.display.flip()
	
	pygame.display.update()


def run():
	global err_label, entered_str, decimals, operators, output
	
	get_input = 1        

	decimals = []
	operators = []
	entered_str = ""
	err_label = ""
	x = -1
	y = -1
	z = -1

	while True:
		events = pygame.event.get()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()		


		draw()
		if get_input:
			if entered_str:
				output=""
			else:	pygame.time.wait(100)
			if events:	
				x = number_button_handler(events[0])
				y = operator_button_handler(events[0])
				z = clear_button_handler(events[0])
			
			no = []
			op = []
			if x!=-1:
				err_label = ""
				no = no + [x]
				pygame.time.wait(100)
			
			for i in no:
				num = number_buttons[i]._propGetCaption()
				store_str(num)
				#pygame.time.wait(2000)
					#print x,number_buttons[x]._propGetCaption()
			if y!=-1:
				err_label = ""
				op+=[y]
				pygame.time.wait(100)
			for i in op:
				opr = operator_buttons[i]._propGetCaption()
				get_input = store_str(opr)
				
			if z!=-1:
				if z==0:
					clear_a_key()
				if z==1:
					clear_all()
				pygame.time.wait(100)
		else:
			entered_str = ""
			run()	



def main():
	init_buttons()
	run()


if __name__=="__main__":	main()
