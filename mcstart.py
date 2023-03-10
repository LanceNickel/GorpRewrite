import sys
import time
import subprocess
import os
import globalvars as v
import config
import test

print('mcstart.py:', v.e, v.o)



class Start:

    #### CONSTRUCTOR
    
    def __init__(self, startServer, ySet):
        self.server = startServer
        self.y = ySet

        self.getConfigItems()







    #### CONFIG AND GUARDS

    ## Get Config

    def getConfigItems(self):
        self.homedir = config.getConfigItem('homedir')
        self.levelName = config.getLevelName(self.server)
        self.doChecks()



    ## Guards
    
    def doChecks(self):
        test.serverExists(self.server, 0, 'mcstart.py')
        test.serverRunning(self.server, 1, 'mcstart.py')

        self.firstTime()
    
    
    
    
    
    
    
    #### FIRST RUN, WORLD GENERATION

    ## Detect if this is first run
    
    def firstTime(self):
        if config.getLinesInProperties(self.server) <= '10':
            self.startServer()
        else:
            self.promptGenerate()



    ## Prompt user to re-generate world if not first run

    def promptGenerate(self):
        if not test.worldExists(self.server, self.levelName):
            response = input("Active world (" + self.levelName + ") doesn\'t exist. Generate new world? [y/n] ") # type: ignore
            response = response.lower()

            if response != 'y':
                if v.e: print('mcstart.py: User cancelled. Exit (19).')
                sys.exit(19)
        
        self.startServer()







    #### START THE SERVER
    
    def startServer(self):
        if v.o: print('Starting server...')


        # Establish paths & cwd

        self.pathToRun = self.homedir + '/servers/' + self.server + '/run.sh'
        self.newDir = self.homedir + '/servers/' + self.server + '/'
        os.chdir(self.newDir)

        # Run Screen

        self.result = subprocess.run(['screen', '-d', '-m', '-S', self.server, self.pathToRun, 'pleasedontdothis'], stdout=subprocess.PIPE)

        # Give 'er a second

        time.sleep(5)

        # Keep reading the log file until "done!"

        path = self.homedir + '/servers/' + self.server + '/logs/latest.log'
        file = open(path, 'r')
        
        i=0

        while True:
            new = file.readline()

            # break if we found patten
            if new:
                if "INFO]: Done (" in new:
                    break
            else:
                i = i+1
                time.sleep(0.01)
            
            # timeout reached (>= 30 seconds with forced 0.01 sleep)
            if i >= 3000:
                if v.o: print('Timeout reached! Use "gorp -t <server>" to see the latest log to investigate further.')
                if v.e: print('mcstart.py: Startup failure. Log did not indicate "done!" before timeout. Exit (36).')
                sys.exit(36)
        
        if v.o: print('Server started!')