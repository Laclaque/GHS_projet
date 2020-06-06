#!/bin/python3

#from multiprocessing import Lock
# lock = Lock() ; lock.acquire() ; lock.release()

# The procedure that writes (append) in a file
# Arguments :
#	- f_name : the name of the file to write in
#	- txt : the text to append to the file
# Returns : None
def write_in_file(f_name, txt):
	if f_name == None:
		return 1
	f_ = open(f_name, "a")
	f_.write(txt)
	f_.flush()
	f_.close()

