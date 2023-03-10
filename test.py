from pathlib import Path
import subprocess
import sys
import globalvars as v
import config







#### SERVER EXISTS

def server_exists(server_name, guard_mode = 2, calling_name = __name__):
    ## Get and test path

    homedir = config.get_config_item('homedir')
    path = f'{homedir}/servers/{server_name}'
    p = Path(path)
    exists = p.exists()

    ## If guard == 0, exit on false

    if guard_mode == 0:
        if not exists:
            if v.e: print(f'{calling_name}.py: Server not found. Exit (30).')
            sys.exit(30)

    ## If guard == 1, exit on true

    elif guard_mode == 1:
        if exists:
            if v.e: print(f'{calling_name}.py: Server already exists. Exit (31).')
            sys.exit(31)
    
    ## If guard not set, return boolean

    else:
        return exists







#### WORLD EXISTS

def world_exists(server_name, world_name, guard_mode = 2, calling_name = __name__):
    ## Get and test path
    
    homedir = config.get_config_item('homedir')
    path = f'{homedir}/servers/{server_name}/{world_name}'
    p = Path(path)
    exists = p.exists()

    ## If guard == 0, exit on false

    if guard_mode == 0:
        if not exists:
            if v.e: print(f'{calling_name}.py: World not found. Exit (40).')
            sys.exit(40)

    ## If guard == 1, exit if true

    elif guard_mode == 1:
        if exists:
            if v.e: print(f'{calling_name}.py: World already exists. Exit (41).')
            sys.exit(41)
    
    ## If guard nt set, return boolean

    else:
        return exists







#### SERVER RUNNING

def server_running(server_name, guard_mode = 2, calling_name = __name__):
    ## Get and store server running status

    check = subprocess.run(['./screencheck.sh', server_name], stdout=subprocess.PIPE)
    check = check.stdout.decode('utf-8').strip()

    ## Test check output & set accordingly

    if check == '1':
        running = True
    else:
        running = False

    ## If guard == 0, exit on false

    if guard_mode == 0:
        if not running:
            if v.e: print(f'{calling_name}.py: Server must be running. Exit (35).')
            sys.exit(35)
    
    ## If guard == 1, exit on true

    elif guard_mode == 1:
        if running:
            if v.e: print(f'{calling_name}.py: Server cannot be running. Exit (34).')
            sys.exit(34)

    ## If guard not set, return boolean

    else:
        return running







#### SHA256 SUM OF FILE

def sha256_sum_file(path):
    import hashlib

    hash = hashlib.sha256()

    file = path

    try:
        with open(file, 'rb') as f:
            for segment in iter(lambda: f.read(4096), b""):
                hash.update(segment)
            return hash.hexdigest()
    except FileNotFoundError:
        return 'dne'