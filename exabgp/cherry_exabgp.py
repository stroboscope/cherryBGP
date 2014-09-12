#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib, sys, time
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read
from select import select
import exceptions

def api_call(cmd):
    try:
        junk=read(sys.stdin.fileno(), 4096)
	#TODO: collect as status messages
    except exceptions.OSError:
	junk=''

    sys.stdout.write(cmd)
    sys.stdout.flush()
    r,_,_ = select([sys.stdin], [], [], 1.0)
    if r:
	return read(sys.stdin.fileno(), 4096)
    return ''


flags = fcntl(sys.stdin, F_GETFL)
fcntl(sys.stdin, F_SETFL, flags | O_NONBLOCK)

server = SimpleXMLRPCServer(("0.0.0.0", 8000),logRequests=False)

server.register_function(api_call, 'api_call')

server.serve_forever()