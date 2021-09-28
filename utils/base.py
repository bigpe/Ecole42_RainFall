import os
import subprocess
from pathlib import Path

from utils.text import print_output

dev_null = open(os.devnull, 'w')
pipe = subprocess.PIPE


def get_previous_password():
    current_level = get_current_level()
    previous_level_num = str(int(current_level[-1:]) - 1).zfill(1)
    previous_level = f'{current_level[:-1]}{previous_level_num}'
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


def save_token(token, client=None):
    prefix = ''
    if 'Ressources' in os.getcwd():
        prefix = '../'
    print_output(token, 'Token to next level')
    open(f'{prefix}flag', 'w').write(token.strip())
    if client:
        client.close()
    save_walkthrough()


def save_walkthrough():
    if os.getcwd().split('/')[-1] == 'Ressources':
        subprocess.Popen('p2j break.py -o -t ../walkthrough.ipynb'.split(' '), stdout=dev_null)
