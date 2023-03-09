import configparser
import subprocess

config = configparser.ConfigParser()
config.sections()
config.read('config.conf')



def gamever():
    return config['CONFIG']['gamever']

def ram():
    return config['CONFIG']['ram']

def homedir():
    return config['CONFIG']['homedir']

def backupDest():
    return config['CONFIG']['backup_dest']

def archiveDest():
    return config['CONFIG']['archive_dest']



def levelName(serverName):
    path = homedir() + '/servers/' + serverName + '/server.properties'

    with open(path) as f:
        for line in f:
            if 'level-name=' in line:
                line = ' '.join(line.splitlines())
                line = line.strip()
                line = line.replace('level-name=', '')
                return line



def linesInProperties(serverName):
    path = homedir() + '/servers/' + serverName + '/server.properties'

    result = subprocess.run(['cat', path, 'wc', '-l'], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    result = result.strip()

    return result