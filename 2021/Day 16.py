from Functions import get_input


def bin_convert(x):
    """Converts a single character hex string into a 4 digit binary string with leading zeros."""
    assert type(x) == str

    # Convert to decimal
    decimal = int(x, 16)

    # Convert to binary
    bin_d = bin(decimal)

    ans = bin_d[2:].zfill(4)

    return ans


def unpack_input(hex_string):
    ans = ''
    for num in hex_string:
        ans += bin_convert(num)
    return ans


def get_packet_version(x):
    p = x[0:3]
    ans = int(p, 2)
    return ans


def get_packet_type(x):
    p = x[3:6]
    ans = int(p, 2)
    return ans


def main():
    hex_string = get_input('line')[0]
    bin_string = unpack_input(hex_string)

    get_packet_type(bin_string)


main()
