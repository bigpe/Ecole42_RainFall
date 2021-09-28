import os
import subprocess
from pathlib import Path
import paramiko
from paramiko.client import SSHClient

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

def get_previous_password():
    current_level = get_current_level()
    previous_level_num = str(int(current_level[-1:]) - 1).zfill(1)
    previous_level = f'{current_level[:-2]}{previous_level_num}'
    password = Path(f'../../').joinpath(previous_level).joinpath('flag').open().read()
    return password


def get_current_level_num():
    current_level = get_current_level()
    current_level_num = str(int(current_level[-1:])).zfill(1)
    return current_level_num


def get_current_level():
    level_dir_index = 0
    for i, d in enumerate(os.getcwd().split('/')):
        if 'level' in d:
            level_dir_index = i
            break
    current_level = os.getcwd().split('/')[level_dir_index]
    return current_level


def connect_by_previous():
    current_level = get_current_level()
    password = get_previous_password()
    return connect(current_level, password)


def exec(client: SSHClient, command: str, title: str = None, err=False, read_method='readlines'):
    if title:
        print_title(title)
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

    dev_null = open(os.devnull, 'w')
    pipe = subprocess.PIPE

    def pipe_or_null(flag):
        return pipe if flag else dev_null

    command = f"{connect_command} {command}"
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
    if isinstance(commands, str):
        commands_inline = bytes(commands + '\n', 'utf-8')
    output = stream.communicate(input=commands_inline)
    stream.terminate()
    return output[0].decode('utf-8')


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


def save_token(token):
    print_output(token, 'Token to next level')
    open('../flag', 'w').write(token)


def download_from(file_name: str):
    command = f'sshpass -p {get_previous_password()} scp -o StrictHostKeyChecking=no -o ' \
              f'UserKnownHostsFile=/dev/null -P {VM_PORT} {get_current_level()}@{VM_ADDRESS}:~/{file_name} .'
    print_title(f'Download file {file_name}')
    print_action(command)
    subprocess.call(command.split(' '), stderr=open(os.devnull, 'w'))
    os.chmod(file_name, 0o777)