import colorama
import random
from typing import Union

colored = True


def disable_color():
    global colored
    colored = False


def print_title(text: str):
    if colored:
        print(f'{colorama.Fore.YELLOW}{text}{colorama.Fore.RESET}')
    else:
        print(text)


def print_action(text: str):
    if colored:
        print(f'{colorama.Fore.CYAN}Execute command: {colorama.Fore.RESET}'
              f'{colorama.Fore.GREEN}{text}{colorama.Fore.RESET}')
    else:
        print(f'Execute command: {text}')


def print_output(text: Union[str, list], prefix: str = None):
    if prefix:
        prefix = f'{prefix}: '
    else:
        prefix = ''
    p = lambda txt: print(f'{prefix}{colorama.Fore.MAGENTA}{txt.strip()}{colorama.Fore.RESET}')
    if isinstance(text, str):
        if colored:
            p(text)
        else:
            print(f'{prefix}{text.strip()}')
    if isinstance(text, bytes):
        if colored:
            p(text.decode('utf-8'))
        else:
            print(f'{prefix}{text.decode("utf-8").strip()}')
    if isinstance(text, list):
        for t in text:
            if colored:
                p(t)
            else:
                print(f'{prefix}{t.strip()}')


def print_magic(text: str):
    colors = [
        colorama.Fore.CYAN,
        colorama.Fore.GREEN,
        colorama.Fore.BLUE,
        colorama.Fore.MAGENTA,
        colorama.Fore.WHITE,
        colorama.Fore.RED
    ]
    for i, t in enumerate(text):
        end = '' if i + 1 != len(text) else '\n'
        if colored:
            print(f'{random.choice(colors)}{t}{colorama.Fore.RESET}', end=end)
        else:
            print(t, end=end)
