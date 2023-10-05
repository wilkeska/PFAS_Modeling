
import os
import sys
import time
from settings import output_folder

if os.path.exists(output_folder) == False: #check if output folder exists
    os.makedirs(output_folder) #create output folder if it doesn't exist

file = open(f'{output_folder}/log.txt', 'w') #create log file
file.close() #close log file

def myprint(txt): #print to console and log file
    print(txt, file=open(f'{output_folder}/log.txt', 'a'))
    print(txt)
    file.close()
    
def myinput(txt): #input to console and log file
    inp = input(txt)
    print(txt+inp, file=open(f'{output_folder}/log.txt', 'a'))
    file.close()
    return inp




# restart function only works for executable, not in python interpreter
def restart_main():
    executable = sys.executable
    executable_filename = os.path.split(executable)[1]
    os.execv(executable, sys.argv)

while os.system('dot -V') == 1:
    myprint('graphviz must be installed on your PATH to generate reaction pathway diagrams')
    time.sleep(1)
    myinput('press enter to launch graphviz installer')
    
    path_to_file = 'files/'
    exe = 'graphviz-install.exe'
    cur_dir = os.getcwd()
    os.chdir(path_to_file) # change folder
    os.system(f'{exe}')
    os.chdir(cur_dir) # go back
    
    myprint('graphviz installed -> restarting PFRTP run...')
    
    restart_main()

