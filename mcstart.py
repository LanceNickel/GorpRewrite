import sys
import time
import subprocess
import os
import globalvars as v
import config
import test



class Start:

    #### CONSTRUCTOR
    
    def __init__(self, startServer, ySet):
        self.server = startServer
        self.y = ySet

        self.get_config_items()







    #### CONFIG AND GUARDS

    ## Get Config

    def get_config_items(self):
        self.homedir = config.get_config_item('homedir')
        self.levelName = config.get_level_name(self.server)
        self.checks()



    ## Guards
    
    def checks(self):
        test.server_exists(self.server, 0, __name__)
        test.server_running(self.server, 1, __name__)

        self.check_first_time()
    
    
    
    
    
    
    
    #### FIRST RUN, WORLD GENERATION

    ## Detect if this is first run
    
    def check_first_time(self):
        if config.get_lines_in_properties(self.server) <= '10':
            self.startServer()
        else:
            self.promptGenerate()



    ## Prompt user to re-generate world if not first run

    def promptGenerate(self):
        if not test.world_exists(self.server, self.levelName):
            response = input(f"Active world ({self.levelName}) doesn't exist. Generate new world? [y/n] ") # type: ignore
            response = response.lower()

            if response != 'y':
                if v.e: print('mcstart.py: User cancelled. Exit (19).')
                sys.exit(19)
        
        self.startServer()







    #### START THE SERVER
    
    def startServer(self):
        if v.o: print('Starting server...')


        ## Establish paths and cwd

        path_to_run = f'{self.homedir}/servers/{self.server}/run.sh'
        new_dir = f'{self.homedir}/servers/{self.server}/'
        path_to_log = f'{self.homedir}/servers/{self.server}/logs/latest.log'
        os.chdir(new_dir)



        ## Get SHA256 of current log file

        original_sum = test.sha256_sum_file(path_to_log)

        
        
        ## Run Screen

        self.result = subprocess.run(['screen', '-d', '-m', '-S', self.server, path_to_run, 'pleasedontdothis'], stdout=subprocess.PIPE)

        
        
        ## Wait for new log file to be created

        i=0

        while original_sum == test.sha256_sum_file(path_to_log):
            i = i+0.5
            if (i >= 10): # 10 seconds at least
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
        


        ## We're done!
        
        if v.o: print('Server started!')