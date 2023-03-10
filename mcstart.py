import sys
import time
import subprocess
import os
import config
import checks as check



class Start:

    def __init__(self, startServer, ySet):
        self.server = startServer
        self.y = ySet
        self.getConfigItems()
    


    def getConfigItems(self):
        self.homedir = config.getConfigItem('homedir')
        self.levelName = config.getLevelName(self.server)
        self.doChecks()
    


    def doChecks(self):

        if not check.serverExists(self.server):
            print('mcstart.py: Server not found. Exit (30).')
            sys.exit(30)

        if check.running(self.server):
            print('mcstart.py: Server already running. Exit (33).')
            sys.exit(33)

        self.firstTime()
    


    def firstTime(self):
        if config.getLinesInProperties(self.server) == '1':
            self.startServer()
        else:
            self.promptGenerate()



    def promptGenerate(self):
        if not check.worldExists(self.server, self.levelName):
            response = input("Active world (" + self.levelName + ") doesn\'t exist. Generate new world? [y/n] ") # type: ignore

            response = response.lower()

            if response != 'y':
                print('mcstart.py: User cancelled. Exit (19).')
                sys.exit(19)
        
        self.startServer()
    


    def startServer(self):
        print('Starting server...')

        self.pathToRun = self.homedir + '/servers/' + self.server + '/run.sh'
        self.newDir = self.homedir + '/servers/' + self.server + '/'

        os.chdir(self.newDir)

        self.result = subprocess.run(['screen', '-d', '-m', '-S', self.server, self.pathToRun, 'pleasedontdothis'], stdout=subprocess.PIPE)
        self.result = self.result.stdout.decode('utf-8')
        self.result = self.result.strip()

        time.sleep(5)

        ## follow log file
        path = self.homedir + '/servers/' + self.server + '/logs/latest.log'
        file = open(path, 'r')
        
        i=0

        while True:
            new = file.readline()

            if new:
                if "INFO]: Done (" in new:
                    break
            else:
                i = i+1
                time.sleep(0.01)
            
            if i >= 3000:
                print('mcstart.py: Startup failure. Log did not indicate "done!" before timeout. Exit (36).')
                sys.exit(36)
        
        print('Server started!')