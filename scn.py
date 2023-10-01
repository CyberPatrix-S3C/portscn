#!/usr/bin/env python

# imports
import os
import argparse
import socket #for connecting
from  colorama import init, Fore
from queue import Queue
from threading import Thread, Lock

# some colors
init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GREY = Fore.LIGHTBLACK_EX

# Number of threads
N_THREADS = 200 # thread queue
q = Queue()
print_lock = Lock()

# =====================================================

#--- clear function
def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
clear()

__author__ = Fore.WHITE+"CyberPatriX-S3C"
__version__ = Fore.WHITE+"1.0.3"


# Banner
print (Fore.GREEN+'''

8""""8                   8""""8 8""""8 8"""8 
8    8 eeeee eeeee eeeee 8      8    " 8   8 
8eeee8 8  88 8   8   8   8eeeee 8e     8e  8 
88     8   8 8eee8e  8e      88 88     88  8 
88     8   8 88   8  88  e   88 88   e 88  8 
88     8eee8 88   8  88  8eee88 88eee8 88  8 
                                             

''')

__info = '''
---[ {c}Version :  {v}           ]---
---[ {c}Author :  {a}  ]---
'''.format(a=__author__, v=__version__, c=Fore.GREEN)

print (__info)

infoBox = Fore.GREEN+f"""
 ==================[ INFO ]========================
|       NOTE: To check for updates type;           |
|               {Fore.WHITE} python update.py{Fore.GREEN}                  |
|                 Scan For                         |
|             Open/Close Ports                     |
 ==================================================
"""
print (infoBox)


# ======================================================

def port_scan(port):
	"""Scan a port on the global variable 'host' """
	try:
		s = socket.socket()
		s.connect((host, port))
	except:
		with print_lock:
			print (f"{GREY}[-] {host:15} : {port:5} is CLOSED {RESET}", end = "\r")
	else:
		with print_lock:
			print (f"{GREEN}[+] {host:15} : {port:5} is OPEN {RESET}")
	finally:
		s.close()

def scan_thread():
	global q
	while True:
		# get the port number from the queue
		worker = q.get()
		# scan that port numbee
		port_scan(worker)
		# tells the queue that the scanning for that port is done
		q.task_done()

def main(host, ports):
	global q

	for t in range(N_THREADS):
		# for each thread, start it
		t = Thread(target=scan_thread)
		# when we set daemon to true, that thread will end when
		# the main thread ends
		t.daemon = True
		# start the daemon thread
		t.start()
	
	for worker in ports:
		# for each porta, put that port into the queue
		# to start scanning.
		q.put(worker)
	
	# wait for the threads (port scanners) to finish
	q.join()

if __name__ == "__main__":
	# parse some parameters passed
	parser = argparse.ArgumentParser(description = "Port Scanner")
	parser.add_argument("host", help="Host to scan")
	parser.add_argument("--ports", "-p", dest="port_range", default="1-65535", help="port range to scan, default 1-65535 (all ports)")

	args = parser.parse_args()
	host, port_range = args.host, args.port_range
	start_port, end_port = port_range.split("-")
	start_port, end_port = int(start_port), int(end_port)
	ports = [p for p in range(start_port, end_port)]
	main(host, ports)
