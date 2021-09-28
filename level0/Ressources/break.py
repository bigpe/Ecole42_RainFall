import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect, exec_in_stream, exec_stream
from utils.text import print_output, print_title
from utils.base import save_token

client = connect('level0', 'level0')

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

output = exec(client, './level0', err=True, title='Simple execute binary')
print_output(output, 'Output')
print_title('Nothing happened')

output = exec(client, './level0 test', err=True, title='Simple execute binary')
print_output(output, 'Output')
print_title('Okay, expected another args, lets find it')
print_title('Debug Time')

main_structure = exec(client, 'echo "disass main" | gdb ./level0 -q', title='Get structure of main')
print_output(main_structure)
print_title('Many interesting things, cut a little')

for line in main_structure:
    if 'call' in line or 'cmp' in line:
        print_output(line)
print_title('Func get arg, call atoi to reformat it and call cmp to compare it with 0x1a7(423)')
print_title('Later execute command or write error')
print_title('Okay, we obtained the answer - 423 (compare), send it to our binary')

stream = exec_stream('./level0 423', title='Execute binary with expected arg',
                     stdin=True, stdout=True, password='level0')
print_title('Okay, stdin intercepted, shell? Check it out')
output = exec_in_stream(stream, 'whoami', title='Try to call whoami')
print_output(output, 'Current user')
print_title('Level1, nice, find anything in home dir')

stream = exec_stream('./level0 423', stdin=True, stdout=True, password='level0')
output = exec_in_stream(stream, 'ls -la /home/user/level1', title='Show home dir files')
print_output(output)
print_title('.pass file, got it')

stream = exec_stream('./level0 423', stdin=True, stdout=True, password='level0')
token = exec_in_stream(stream, 'cat /home/user/level1/.pass', title='Read .pass file')
print_output(token, 'File content')
print_title('Woo-hoo!')

save_token(token, client)
