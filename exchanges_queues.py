#!/bin/python3

from multiprocessing import queue
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
def send_to(q_,sender,receiver,name,val1,val2,val3,f_)
	obj = {
		"type" : name,
		"val1" : val1,
		"val2" : val2,
		"val3" : val3,
		"sender" : sender
	}
	q_.send(json.dumps(obj))
	txt = register.send_msg(sender,receiver,name,val1,val2,val3)
	fbasics.write_in_file(f_,txt)
	

# The fct to receive a msg from another node (read in queue)
# Arguments :
#	- q_ : the queue to read in 
#	- receiver : the id of the receiver (the one who read in queue)
#	- f_ : the name of the file to register msg in
# Returns :
#	- {"type":_, "val1":_, "val2":_, "val3":_}
def recv_from(q_,receiver,f_):
	obj = q_.get(json.loads(obj))
	txt = (sender,receiver,obj["sender"],obj["type"],obj["val1"],obj["val2"],obj["val3"])
	fbasics.write_in_file(f_,txt)
	return obj
