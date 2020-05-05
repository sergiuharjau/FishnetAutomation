import psutil
import time
import subprocess
import os, signal
import psutil
from datetime import datetime

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def isLocked():
    for proc in psutil.process_iter():
        if(proc.name() == "LogonUI.exe"):
            return True
    return False

hist = open("historical_data.txt", "r")
hist_data = hist.readlines()
totalPositions = int(hist_data[0][:-1])
totalTimeCPU = float(hist_data[1][:-1])
hist.close()

fishnetRunning = False
programStart = time.time()
startTime = time.time()

while True:
    locked = isLocked()
    
    for proc in psutil.process_iter():
        if(proc.name() == "LogonUI.exe"):
            locked = True
            break
    
    if fishnetRunning: # while fishnet is running
        
        if not locked: # when the user unlocks the computer, stop fishnet
            print("[User has logged in. Stopping Stockfish.]")
            fishnetRunning = False 
            kill(fish.pid)

            #Save how many positions we computed
            output = open("stdout.txt", "a")
            dt_string = datetime.now().strftime("%d%m%Y-->%H:%M")
            output.write("\n-->\n[Session Time]\n%s\n\n" % datetime.now().strftime("%d-%m-%Y %H:%M"))
         
            analysis = "Analyzed not even 0 nodes." 
            while True:
                line = fish.stdout.readline().decode()
                if not line:
                    break
                output.write(line[:-1])
                if "Analyzed" in line:
                    analysis = line
            output.close()

            positionsCalculated = int(analysis.split()[3])
                    
            totalPositions += positionsCalculated
            totalTimeCPU += (time.time()-startTime)/3600

            hist = open("historical_data.txt", "w") #for long term storage
            hist.write(str(totalPositions) + "\n")
            hist.write(str(round(totalTimeCPU,2)) + "\n")
            hist.close()
            
            print("\n-->\n[Session calculations: %d positions]" % positionsCalculated)
            print("[Session duration: %.2f minutes]" % round((time.time()-startTime)/60,2))

            print("\n[Total calculations: %d positions]" % totalPositions)
            print("[Total CPU time: %.2f hours]" % totalTimeCPU)
            print("[Program uptime: %.2f hours]\n<--\n" % round((time.time()-programStart)/3600, 2))
                        
            startTime = time.time()
            
    if locked:
        if not fishnetRunning:
            print("\n\n[Screen is locked. Starting Stockfish.]")
            fish = subprocess.Popen("python -m fishnet --auto-update", stdout=subprocess.PIPE, shell=True)
            fishnetRunning = True
            startTime = time.time()
            
        time.sleep(10) # so we have a snappier start when we unlock the computer
    else:
        print("[Waiting on screen lock. Total wait: %d minutes]" % round((time.time()-startTime)/60), end="\r")
        time.sleep(90) # waits 90s to check when user is logged in 
