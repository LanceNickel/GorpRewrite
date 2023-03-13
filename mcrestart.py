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
from mcstop import Stop
from mcstart import Start









class Restart:

    #### CONSTRUCTOR
    
    def __init__(self, restart_server, flag):
        self.server = restart_server
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

        self.restart_coordinator()
    






    #### RESTART COORDINATOR

    def restart_coordinator(self):
        if self.flag == "f":
            functions.warn(self.server, 'restart', 30)
            Stop(self.server, 'n')
            Start(self.server, False)
        
        elif self.flag == "n":
            Stop(self.server, 'n')
            Start(self.server, False)
        
        else:
            # Backup(self.server)
            functions.warn(self.server, 'restart', 5)
            Stop(self.server, 'n')
            Start(self.server, False)