import sys
import config
import checks as check



class Start:

    def __init__(self, startServer, ySet):
        self.server = startServer
        self.y = ySet
        self.getConfigItems()
    


    def getConfigItems(self):
        self.homedir = config.homedir()
        self.levelName = config.levelName(self.server)
        self.doChecks()
    


    def doChecks(self):

        if not check.serverExists(self.server):
            print('mcstart.py: Server not found. Exit (30).')
            sys.exit(30)

        if check.running(self.server):
            print('mcstart.py: Server already running. Exit (33).')
            sys.exit(33)

        if check.worldExists(self.server, self.levelName):
            response = input("Active world (" + self.levelName + ") doesn\'t exist. Generate new world? [y/n] ") # type: ignore

            response = response.lower()

            if response != 'y':
                print('mcstart.py: User cancelled. Exit (19).')
                sys.exit(19)
        
        self.firstTime()
    


    def firstTime(self):
        if config.linesInProperties == '1':
            self.doFirstTime = True
        else:
            self.doFirstTime = False
        
        self.startServer()
    


    def startServer(self):
        
    


