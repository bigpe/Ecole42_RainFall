import sys

arg = sys.argv[1]


def transform_address(address):
    if isinstance(address, bytes):
        address = str(address)
    if ' ' in address:
        address = address.split(' ')[1]
    address = address.replace("'", '')
    address = address[2:]
    res = []
    for i, x in enumerate(address):
        if not i % 2:
            if len(address) > i + 1:
                res.append('\\x{}{}'.format(x, address[i + 1]))
            else:
                res.append('\\x{}'.format(x))
    return ''.join(res[::-1])


if __name__ == '__main__':
    print(transform_address(arg))
