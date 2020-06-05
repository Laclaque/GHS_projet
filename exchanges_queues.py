#!/bin/python3

from multiprocessing import Queue
import json
import files_basics as fbasics
import register

# The procedure to send a msg to another node (write in its queue)
# Arguments :
#	- q_ : the queue to send in
#	- sender : the id of the sender
#	- receiver : the id of the receiver (need to write in file)
#	- name : the type of the message
#	- val1 : the fist value to send
#	- val2 : the second value to send
#	- val3 : the third value to send
#	- f_ : the name of the file to register msg in
# Returns : None
def send_to(q_,sender,receiver,name,val1,val2,val3,f_):
	obj = {
		"type" : name,
		"val1" : val1,
		"val2" : val2,
		"val3" : val3,
		"sender" : sender
	}
	q_.put(json.dumps(obj))
	txt = register.send_msg(sender,receiver,name,val1,val2,val3)
	fbasics.write_in_file(f_,txt)
	

# The fct to receive a msg from another node (read in queue)
# Arguments :
#	- q_ : the queue to read in 
#	- receiver : the id of the receiver (the one who reads in queue)
#	- f_ : the name of the file to register msg in
# Returns :
#	- {"type":_, "val1":_, "val2":_, "val3":_}
def recv_from(q_,receiver,f_):
	obj = json.loads(q_.get())
	txt = register.recv_msg(obj["sender"],receiver,obj["type"],obj["val1"],obj["val2"],obj["val3"])
	fbasics.write_in_file(f_,txt)
	return obj


# The procedure to alert the father the algorithm finished
# Arguments :
#	- q_ : the queue of the father
#	- f_ : the name of the file to register in
# Returns : None
def send_finish(q_, f_):
	q_.put(json.dumps("TERMINE"))
	fbasics.write_in_file(f_, "        TERMINE !!!")

# The fct to receive the alert when algorithm finish
# Arguments :
#	- q : the queue to read in
# Returns : a string
def recv_finish(q_):
	return json.loads(q_.get())
