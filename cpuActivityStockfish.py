import psutil
import time
import subprocess
from datetime import datetime

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def averageActivity():
    cpuActivity=0
    for i in range(6):
        cpuActivity += psutil.cpu_percent()
        time.sleep(5)
        
    return cpuActivity/6

hist = open("historical_data.txt", "r")
hist_data = hist.readlines()
totalPositions = int(hist_data[0][:-1])
totalTimeCPU = float(hist_data[1][:-1])
hist.close()

cpuActivity = 100
programStart = time.time()
startTime = time.time()

print("[The program will assess your CPU's average activity]")
print("[When it drops below 2%, Stockfish will automatically start]")
print("[Data is preserved as part of historical.txt and stdout.txt]\n")

while True:

    if cpuActivity < 2: # while fishnet is running
        kill(fish.pid)

            #Save how many positions we computed
        output = open("stdout.txt", "a")
        output.write("\n-->\n[Session Starting Time]\n%s\n\n" % formattedStartTime)
            
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

    try: 
        cpuActivity = averageActivity()
        print("[Latest CPU Activity %d%%. Total wait: %d minutes]" % (round(cpuActivity), round((time.time()-startTime)/60)), end="\r")        
        if cpuActivity < 2:
            print("\n\n[CPU Activity is low. Starting Stockfish]")
            fish = subprocess.Popen("python -m fishnet --auto-update", stdout=subprocess.PIPE, shell=True)
            startTime = time.time()
            formattedStartTime = datetime.now().strftime("%d%m%Y-->%H:%M")
            try:
                print("[Press CTRL-C when you want Stockfish to stop]") 
                while True:
                    time.sleep(100)  
            except KeyboardInterrupt:
                print("\n[Detected user interrupt. Stopping Stockfish]")
        else:
            time.sleep(90) # waits 90s to check when user is logged in 
    except KeyboardInterrupt:
        print("\n[Shutting down.]")
        break
