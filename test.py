from pathlib import Path
import subprocess
import sys
import globalvars as v
import config

print('test.py:', v.e, v.o)







#### SERVER EXISTS

def serverExists(serverName, guardMode = 2, callingName = 'checks.py', v = 0):
    ## Get and test path

    homedir = config.getConfigItem('homedir')
    path = homedir + '/servers/' + serverName
    p = Path(path)
    exists = p.exists()

    ## If guard == 0, exit on false

    if guardMode == 0:
        if not exists:
            if v < 2: print(callingName + ': Server not found. Exit (30).')
            sys.exit(30)

    ## If guard == 1, exit on true

    elif guardMode == 1:
        if exists:
            if v < 2: print(callingName + ': Server already exists. Exit (31).')
            sys.exit(31)
    
    ## If guard not set, return boolean

    else:
        return exists







#### WORLD EXISTS

def worldExists(serverName, worldName, guardMode = 2, callingName = 'checks.py', v = 0):
    ## Get and test path
    
    homedir = config.getConfigItem('homedir')
    path = homedir + '/servers/' + serverName + '/' + worldName
    p = Path(path)
    exists = p.exists()

    ## If guard == 0, exit on false

    if guardMode == 0:
        if not exists:
            if v < 2: print(callingName + ': World not found. Exit (40).')
            sys.exit(40)

    ## If guard == 1, exit if true

    elif guardMode == 1:
        if exists:
            if v < 2: print(callingName + ': World already exists. Exit (41).')
            sys.exit(41)
    
    ## If guard nt set, return boolean

    else:
        return exists







#### SERVER RUNNING

def serverRunning(serverName, guardMode = 2, callingName = 'checks.py', v = 0):
    ## Get and store server running status

    check = subprocess.run(['./screencheck.sh', serverName], stdout=subprocess.PIPE)
    check = check.stdout.decode('utf-8').strip()

    ## Test check output & set accordingly

    if check == '1':
        running = True
    else:
        running = False

    ## If guard == 0, exit on false

    if guardMode == 0:
        if not running:
            if v < 2: print(callingName + ': Server must be running. Exit (35).')
            sys.exit(35)
    
    ## If guard == 1, exit on true

    elif guardMode == 1:
        if running:
            if v < 2: print(callingName + ': Server cannot be running. Exit (34).')
            sys.exit(34)

    ## If guard not set, return boolean

    else:
        return running