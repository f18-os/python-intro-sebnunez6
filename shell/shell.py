#! /usr/bin/env python3
#Part of code received from Dr. Freudenthal
import os, sys, time, re, signal

def changeDirect(currdir):#method to change directories
    if ".." in command:                
        currdir = ".."
    else:                                         
        currdir = command.split("cd")[1].strip()
    try:                                                #Tries changing to next directory
        os.chdir(currdir)
    except FileNotFoundError:                 
        pass         


def forkExec(rc, piping, r, w,left):   #method to execute fork
    if rc < 0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:                   # child

        if piping and left: #checking for piping and if input for piping
            os.close(r)
            os.dup2(w, sys.stdout.fileno(),True)
        elif piping and not left: #checks if output for piping
            os.close(w)
            os.dup2(r, sys.stdin.fileno(),True)

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
        if(piping):
            os.dup2(1,w,True)
        childPidCode = os.wait()

    pid = os.getpid()               # get and remember pid
    currdir = os.getcwd()

while True:
    currdir = os.getcwd() #gets current directory
    folder = currdir[currdir.rfind("/",0,len(currdir)) + 1:]
    os.write(1, ("@"  + folder + "$ ").encode()) #prints @current folder$ to terminal
    command = input()

    if "exit" in command: #Terminates shelll
        sys.exit(0)

    if "cd" in command:#changes current directory
        changeDirect(command)     
        continue

    if "|" in command:#checks for piping
        r,w = os.pipe()
        left = True
        
        for command in command.split("|"):#creates children for piping
            rc = os.fork()
            forkExec(rc,True,r,w, left)
            left = False
        continue
    
    rc = os.fork()
    forkExec(rc,False, 0,1,False)
