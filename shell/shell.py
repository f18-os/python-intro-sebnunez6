#! /usr/bin/env python3
#Part of code received from Dr. Freudenthal
import os, sys, time, re, signal

pid = os.getpid()               # get and remember pid

#os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
currdir = os.getcwd()
while True:
    folder = currdir[currdir.rfind("/",0,len(currdir)) + 1:]
    os.write(1, ("@"  + folder + "$ ").encode()) #prints $ to terminal
    command = input()

    if "exit" in command: #Terminates shelll
        sys.exit(0)

    if "cd" in command:
    
        if ".." in command:                 #gets rid of last directory in path
            currdir = currdir[:currdir.rfind("/",0,len(currdir))]

        else:                                           #adds new directory to path
            currdir = currdir + "/" + command.split("cd")[1].strip()
    
        try:                                                #Tries changing to next directory
            os.chdir(currdir)
        except FileNotFoundError:                 
            pass                                 
        continue
    
    else:
        rc = os.fork()
    
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child
        redirectionTester = command.split(">") #checks for output redirection
        inputdirection = command.split("<")

        if len(redirectionTester)  > 1:# redirect child's stdout
            inputdirection = redirectionTester[0].split("<")
            os.close(1)                
            sys.stdout = open(redirectionTester[1].strip(), "w")  
            fd = sys.stdout.fileno() 
            os.set_inheritable(fd, True)

        if len (inputdirection) > 1: #turn file text into system arguements 
            args = inputdirection[0].split()
            os.close(0)                
            sys.stdin = open(inputdirection[1].strip(), "r")  
            fd = sys.stdin.fileno() 
            os.set_inheritable(fd, True)
       
        else:                                           #no redirection
            args = inputdirection[0].split()
        if len(args) < 1:
            sys.exit(1)

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
        #os.write(1, ("Command executed\n".encode()))
