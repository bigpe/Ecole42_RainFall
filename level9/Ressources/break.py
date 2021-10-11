import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, find_offset, get_func_address, get_func_structure, exec_stream, \
    exec_in_stream
from utils.text import print_output, print_title
from utils.base import save_token, get_buffer_overflow_command, address_to_string

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

binary_name = files_list[0]

