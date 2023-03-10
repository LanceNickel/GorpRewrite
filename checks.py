from pathlib import Path
import subprocess
import config



homedir = config.getConfigItem('homedir')



def serverExists(serverName):
    path = homedir + '/servers/' + serverName
    p = Path(path)
    return p.exists()



def worldExists(serverName, worldName):
    path = homedir + '/servers/' + serverName + '/' + worldName
    p = Path(path)
    return p.exists()



def running(serverName):
    result = subprocess.run(['./screencheck.sh', serverName], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    result = result.strip()

    if result == '1':
        return True
    else:
        return False