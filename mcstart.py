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



import sys
import time
import subprocess
import os
import globalvars as v
import config
import functions









class Start:

    #### CONSTRUCTOR
    
    def __init__(self, start_server, y_set):
        self.server = start_server
        self.y = y_set

        self.get_config_items()









    #### CONFIG AND GUARDS

    ## Get Config

    def get_config_items(self):
        self.homedir = config.get_config_item('homedir')
        self.level_name = config.get_level_name(self.server)
        self.guards()



    ## Guards
    
    def guards(self):
        functions.server_exists(self.server, 0, __name__)
        functions.server_running(self.server, 1, __name__)
        functions.jar_exists(self.server, 0, __name__)

        self.check_first_time()
    
    
    
    
    


    
    
    #### FIRST RUN, WORLD GENERATION

    ## Detect if this is first run
    
    def check_first_time(self):
        if config.get_lines_in_properties(self.server) <= '10':
            self.start_server()
        else:
            self.prompt_generate()



    ## Prompt user to re-generate world if not first run

    def prompt_generate(self):
        if not functions.world_exists(self.server, self.level_name):
            response = input(f"Active world ({self.level_name}) doesn't exist. Generate new world? [y/n] ") # type: ignore
            response = response.lower()

            if response != 'y':
                if v.e: print('mcstart.py: User cancelled. Exit (19).')
                sys.exit(19)
        
        self.start_server()









    #### START THE SERVER
    
    def start_server(self):
        if v.o: print('Starting server...')


        ## Establish paths and cwd

        path_to_run = f'{self.homedir}/servers/{self.server}/run.sh'
        new_dir = f'{self.homedir}/servers/{self.server}/'
        path_to_log = f'{self.homedir}/servers/{self.server}/logs/latest.log'
        os.chdir(new_dir)



        ## Get SHA256 of current log file

        original_sum = functions.sha256_sum_file(path_to_log)

        
        
        ## Run Screen

        self.result = subprocess.run(['screen', '-d', '-m', '-S', self.server, path_to_run, 'pleasedontdothis'], stdout=subprocess.PIPE)

        
        
        ## Wait for new log file to be created

        if v.d: print('Waiting for log file...')

        i=0

        while original_sum == functions.sha256_sum_file(path_to_log):
            i = i+0.5
            if i >= 10: # 10 seconds at least
                if v.e: print('mcstart.py: Startup failure. Log was not created before timeout. Exit (36).')
                sys.exit(36)
            
            time.sleep(0.5)
        
        
        
        ## Try to open the new log file

        try:
            file = open(path_to_log, 'r')
        
        except FileNotFoundError:
            if v.e: print('mcstart.py: Unable to locate log file to monitor. Server is likely running but is in an unknown state. Exit (36).')
            sys.exit(36)
            
        

        ## Follow the file until match

        i=0

        while True:
            new = file.readline()

            # break if we found patten
            if new:

                if v.d: print(new.strip())

                if "INFO]: Done (" in new:
                    break
            else:
                i = i+1
                time.sleep(0.001)
            
            # timeout reached (>= 30 seconds with forced 0.001 sleep)
            if i >= 30000:
                if v.o: print('Timeout reached! Use "gorp -t <server>" to see the latest log to investigate further.')
                if v.e: print('mcstart.py: Startup failure. Log did not indicate "done!" before timeout. Exit (36).')
                sys.exit(36)
        


        ## We're done!
        
        if v.o: print('Server started!')