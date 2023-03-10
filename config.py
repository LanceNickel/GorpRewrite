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



import configparser
import subprocess
import sys
import globalvars as v



config = configparser.ConfigParser()
config.sections()
config.read('config.conf')



def get_config_item(key):
    try:
        return config['CONFIG'][key]
    except:
        print('config.py: Configuration item not found. Exit (2).')
        sys.exit(2)



def get_level_name(server_name):
    homedir = get_config_item('homedir')
    path = f'{homedir}/servers/{server_name}/server.properties'

    try:
        with open(path) as f:
            for line in f:
                if 'level-name=' in line:
                    line = ' '.join(line.splitlines()).strip().replace('level-name=', '')
                    return line
    except:
        pass
    



def get_lines_in_properties(server_name):
    homedir = get_config_item('homedir')
    path = f'{homedir}/servers/{server_name}/server.properties'

    cat = subprocess.Popen(('cat', path), stdout=subprocess.PIPE)
    wc = subprocess.run(('wc', '-l'), stdin=cat.stdout, stdout=subprocess.PIPE)
    cat.wait()

    result = wc.stdout.decode('utf-8').strip()

    return result