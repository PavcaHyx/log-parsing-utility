# App for parsing of logs

## Python CLI application that can help parse logs of various kinds

Usage: `./util.py [OPTION]... [FILE]`

### Supported options:

 * -h, --help         Print help
 * -f, --first=NUM    Print first NUM lines
 * -l, --last=NUM     Print last NUM lines
 * -t, --timestamps   Print lines that contain a timestamp in HH:MM:SS format
 * -i, --ipv4         Print lines that contain an IPv4 address, matching IPs are highlighted
 * -I, --ipv6         Print lines that contain an IPv6 address (standard notation), matching IPs are highlighted
