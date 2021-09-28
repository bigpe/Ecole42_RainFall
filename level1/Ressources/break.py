import os
import sys
bool('Ressources' in os.getcwd()) if sys.path.append("../") else sys.path.append("../..")
from utils.ssh import exec, connect_by_previous, exec_in_stream, exec_stream
from utils.text import print_output, print_title
from utils.base import save_token

client = connect_by_previous()

files_list = exec(client, 'ls', title='Get files list')
print_output(files_list, 'Files')
print_title('Test this file')

stream = exec_stream('./level1', title='Simple execute binary', stdin=True)
print_title('Okay, stdin intercepted, stdin write expected')

output = exec_in_stream(stream, 'test', title='Send test in stdin')
print_output(output)
print_title('Nothing happened')
print_title('Debug Time')
