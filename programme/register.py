#!/bin/python3
import files_basics as fb

# The fct to create a string about msg sent
# Arguments :
#	- sender : the sender id
#	- receiver : the receiver id
#	- name : the type of msg
#	- val1 : first value
#	- val2 : second value
#	- val3 : third value
#	- f_ : the file to write in
# Returns : None
def send_msg(sender, receiver, name, val1, val2, val3, f_):
	txt = "        "+format(sender)+" envoie à "+format(receiver)+" : ("+format(name)+", "+format(val1)+", "+format(val2)+", "+format(val3)+") ...\n"
	print(txt)
	fb.write_in_file(f_, txt)

# The fct to create a string about msg rcved
# Arguments :
#	- sender : the sender id
#	- receiver : the receiver id
#	- name : the type of msg
#	- val1 : first value
#	- val2 : second value
#	- val3 : third value
#	- f_ : the file to write in
# Returns : None
def recv_msg(sender, receiver, name, val1, val2, val3, f_):
	txt = format(receiver)+" recoit de "+format(sender)+" : ("+format(name)+", "+format(val1)+", "+format(val2)+", "+format(val3)+") ...\n"
	fb.write_in_file(f_, txt)

# The fct to create a string about value var changed
# Arguments :
#	- name : the name of the changed var
#	- old : the old value
#	- new :  the new value
#	- f_ : the file to write in
# Returns : None
def change_var(name, old, new, f_):
	txt = "        "+format(name)+" : "+format(old)+" --> "+format(new)+"\n"
	fb.write_in_file(f_, txt)

# The fct to register a set_
# Arguments :
#	- set_ : the set to register
#	- f_ : the file to write in
# Returns : None
def set_state(set_, f_):
	fb.write_in_file(f_, "--------\nSet state :\n")
	for x, y in set_.items():
		if x != "queues": # We don't want to register the queues
			fb.write_in_file(f_, format(x)+" : "+format(y)+"\n")
	fb.write_in_file(f_, "--------\n\n")
