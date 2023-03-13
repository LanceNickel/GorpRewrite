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
import globalvars as v
# from mcbackup import Backup
import functions
import config









class Stop:

    #### CONSTRUCTOR
    
    def __init__(self, stop_server, flag):
        self.server = stop_server
        self.flag = flag

        self.get_config_items()









    #### CONFIG AND GUARDS

    # Get Config

    def get_config_items(self):
        self.homedir = config.get_config_item('homedir')
        self.guards()



    # Guards
    
    def guards(self):
        functions.server_exists(self.server, 0, __name__)
        functions.server_running(self.server, 0, __name__)

        self.stop_coordinator()
    






    #### STOP COORDINATOR

    def stop_coordinator(self):
        if self.flag == "f":
            functions.warn(self.server, 'stop', 30)
            self.stop_server()
        
        elif self.flag == "n":
            self.stop_server()
        
        else:
            # Backup(self.server)
            functions.warn(self.server, 'stop', 5)
            self.stop_server()







    #### STOP THE SERVER
    
    def stop_server(self):
        if v.o: print('Stopping server...')


        ## Establish paths

        path_to_log = f'{self.homedir}/servers/{self.server}/logs/latest.log'

        ## Issue stop command

        subprocess.run(['screen', '-S', self.server, '-X', 'stuff', 'stop\n'])      
        
        ## Try to open the new log file

        try:
            file = open(path_to_log, 'r')
        
        except FileNotFoundError:
            if v.e: print('mcstop.py: Unable to locate log file to monitor. Server is likely stopped but is in an unknown state. Exit (37).')
            sys.exit(37)
            

        ## Follow the file until match

        i=0

        while True:
            new = file.readline()

            # break if we found patten
            if new:

                if v.d: print(new.strip())

                if "INFO]: Closing Server" in new:
                    break
            else:
                i = i+1
                time.sleep(0.001)
            
            # timeout reached (>= 30 seconds with forced 0.001 sleep)
            if i >= 30000:
                if v.o: print('Timeout reached! Use "gorp -t <server>" to see the latest log to investigate further.')
                if v.e: print('mcstop.py: Shutdown failure. Log did not indicate "closing" before timeout. Exit (37).')
                sys.exit(37)
        

        ## Ensure screen terminates

        i=0
        while i < 5:
            time.sleep(1)
            i = i+1

            enter = subprocess.run(['screen', '-S', self.server, '-X', 'stuff', '\n'], stdout=subprocess.PIPE)
            enter = enter.stdout.decode('utf-8').strip()

            if enter == 'No screen session found.':
                break
            

        


        ## We're done!
        
        if v.o: print('Server stopped!')