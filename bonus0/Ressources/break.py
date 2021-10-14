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

print_action(f'./{binary_name}')
print_action('test', stdin=True)
print_action('test', stdin=True)
print_output('test test', 'Output')
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


# shell_call_address = find_offset(client, stdin=True, pattern=f"\n01234567890123456789\n{PATTERN}", register='eip')

