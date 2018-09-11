#! /usr/bin/env python3
#Part of code received from Dr. Freudenthal
import os, sys, time, re, signal

pid = os.getpid()               # get and remember pid

#os.write(1, ("About to fork (pid=%d)\n" % pid).encode())

while True:
    rc = os.fork()
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        os.write(1, (">".encode()))
        command = input()

        if "kill" in command: #Terminates shelll
            os.kill(os.getppid(), signal.SIGKILL)
            sys.exit(0)

        redirectionTester = command.split(">") #checks for output redirection
        inputdirection = command.split("<")

        if len(redirectionTester)  > 1:# redirect child's stdout
            inputdirection = redirectionTester[0].split("<")
            os.close(1)                
            sys.stdout = open(redirectionTester[1].strip(), "w")  
            fd = sys.stdout.fileno() 
            os.set_inheritable(fd, True)

        if len (inputdirection) > 1: #turn file text into system arguements 
            input = open(inputdirection[1].strip(), "r") 
            str = input.read()
            args = inputdirection[0].split() + str.split()
       
        else:                                           #no redirection
            args = inputdirection[0].split()
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
