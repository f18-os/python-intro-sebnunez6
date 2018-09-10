#! /usr/bin/env python3
#Part of code received from Dr. Freudenthal
import os, sys, time, re

pid = os.getpid()               # get and remember pid

os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

rc = os.fork()

if rc < 0:
    os.write(2, ("fork failed, returning %d\n" % rc).encode())
    sys.exit(1)

elif rc == 0:                   # child
    os.write(1, ("Please enter input\n".encode()))
    command = input()
    redirectionTester = command.split(">")
    inputdirection = command.split("<")
    if len(redirectionTester)  > 1:
        os.close(1)                
        sys.stdout = open(redirectionTester[1].strip(), "w")  # redirect child's stdout
        fd = sys.stdout.fileno() 
        os.set_inheritable(fd, True)
        args = redirectionTester[0].split()
    elif len (inputdirection) > 1:
        input = open(inputdirection[1].strip(), "r") 
        str = input.read()
        args = inputdirection[0].split() + str.split()
    else:
        args = command.split()
    for dir in re.split(":", os.environ['PATH']):  # try each directory in path
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ)  # try to exec program
        except FileNotFoundError:                 # ...expected
            pass                                  # ...fail quietly 

    os.write(2, ("Child:    Error: Could not exec %s\n" % args[0]).encode())
    sys.exit(1)                 # terminate with error

else:                           # parent fork 
    childPidCode = os.wait()
    os.write(1, ("Command executed\n".encode()))
