#!/bin/python3

#from multiprocessing import Lock
# lock = Lock() ; lock.acquire() ; lock.release()

# The procedure to write (append) in a file shared between processes
# Arguments :
#	- f_name : the name of the file to read in
#	- f_lock : the lock associated to the file
#	- txt : the texte to append to the file
def write_in_shared_file(f_name, f_lock, txt):
	f_lock.acquire()
	f_ = open(f_name, "a")
	f_.write(txt)
	f_.flush()
	f_.close()
	f_.release()
