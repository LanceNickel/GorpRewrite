"""
Gorp - Simple Minecraft CLI tools.
    Copyright (C) 2023  Lance Nickel

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""



from pathlib import Path
import subprocess
import sys
import time
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
    
    ## If guard not set, return boolean

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









#### TEST SERVER'S SET JAR EXISTS

def jar_exists(server_name, guard_mode = 2, calling_name = __name__):
    # Get and create path to run.sh
    
    homedir = config.get_config_item('homedir')
    path = f'{homedir}/servers/{server_name}/run.sh'

    # Initialize vars

    exists = False
    path_to_jar = ''

    # Look for the JAR file

    try:
        with open(path) as f:
            for line in f:
                if 'CUSTOM_JAR=' in line:
                    if '# Default:' in line:
                        pass
                    else:
                        path_to_jar = ' '.join(line.splitlines()).strip().replace('CUSTOM_JAR=', '')
                
    except FileNotFoundError:
        if v.e: print(f'{calling_name}.py: Cannot check if JAR exists as server\'s run.sh file does not exist either.')
    

    # Check if specified JAR file exists

    p = Path(path_to_jar)
    exists = p.exists()

    # If guard == 0, exit on False

    if guard_mode == 0:
        if not exists:
            if v.e: print(f'{calling_name}.py: JAR file does not exist for server. Exit (63).')
            sys.exit(63)

    # If guard == 1, exit on True
    
    elif guard_mode == 1:
        if exists:
            if v.e: print(f'{calling_name}.py: JAR already exists. Exit (64).')
            sys.exit(64)

    # If guard not set, return boolean
    
    else:
        return exists









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







#### SEND WARNING IN GAMECHAT

def warn(server_name, action, sleep_time):
    
    if action == 'stop':
        if v.o: print(f'Giving {sleep_time} seconds warning...')

        ## Send warning

        subprocess.run(['screen', '-S', server_name, '-X', 'stuff', 'say This server will shut down in 30 seconds.\n'])

        ## Wait 30 seconds

        i=0

        while i <= sleep_time:
            time.sleep(1)
            i = i+1
            sys.stdout.write(f'\033[K  {i} s\r')