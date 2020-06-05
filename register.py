#!/bin/python3

import files_basics as fbasics

# The fct to create a string about msg sent
# Arguments :
#	- sender : the sender id
#	- receiver : the receiver id
#	- name : the type of msg
#	- val1 : first value
#	- val2 : second value
#	- val3 : third value
# Returns : a string
def send_msg(sender, receiver, name, val1, val2, val3):
	txt = "        "+format(sender)+" envoie à "+format(receiver)+" : ("+format(name)+", "+format(val1)+", "+format(val2)+", "+format(val3)+") ...\n"
	return txt

# The fct to create a string about msg rcved
# Arguments :
#	- sender : the sender id
#	- receiver : the receiver id
#	- name : the type of msg
#	- val1 : first value
#	- val2 : second value
#	- val3 : third value
# Returns : a string
def recv_msg(sender, receiver, name, val1, val2, val3):
	txt = format(receiver)+" recoit de "+format(sender)+" : ("+format(name)+", "+format(val1)+", "+format(val2)+", "+format(val3)+") ...\n"
	return txt

# The fct to create a string about value var changed
# Arguments :
#	- name : the name of the changed var
#	- old : the old value
#	- new :  the new value
def change_var(name, old, new):
	txt = "        "+format(name)+" : "+format(old)+" --> "+format(new)+"\n"
	return txt 

