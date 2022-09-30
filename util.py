import argparse
import os
import sys
import re


# Setting of colors to highlight IP matches in terminal from collections import deque
def set_colors():
    if os.name == 'nt':  # windows
        os.system('color')
    dict_colors = {'ipv4': '\x1b[0;36m', 'ipv6': '\x1b[0;31m', 'end': '\x1b[0m'}
    return dict_colors

# Regular expressions to identify IPv4, IPv6 and timestamp (HH:MM:SS)
def set_regex():
    re_ipv4 = '((?<![\\d\\.])(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][' \
              '0-9]?)(?![\\.\\d]))'
    re_ipv6 = '((?<![:A-Fa-f0-9])(?:[A-Fa-f0-9]{0,4}:){7}[A-Fa-f0-9]{0,4}(?![:A-Fa-f0-9]))'
    re_timestamp = '(?<![:0-9])(?:[01][0-9]|2[0-3])(?::[0-5][0-9]){2}(?![:0-9])'
    return re_ipv4, re_ipv6, re_timestamp



#find out whatever line contains regex
def find_pattern(regex, line):
    if re.search(regex, line):
        return True
    return False

#find out if searched regex is in line
def is_searched_pattern_in_line(dict_regexp, line):
    results = []
    for regexp in dict_regexp.values():
        if find_pattern(regexp, line):
            results.append(True)
        else:
            results.append(False)
            break
    return results

def get_first_lines(inserted_file, count_of_lines):
    if count_of_lines <= 0:
        return []
    else:
        first_num_lines = []
        current_line = 0
        for line in inserted_file:
            current_line += 1
            if current_line <= count_of_lines:
                first_num_lines.append(line)
            else:
                break
    return first_num_lines


def count_of_lines_in_file(inserted_file):
    count_of_lines_in_file = sum(1 for line in inserted_file)
    return count_of_lines_in_file


def get_last_lines(inserted_file, count_of_lines, last_line):
    if count_of_lines <= 0:
        return []
    else:
        current_line = 0
        last_num_lines = []
        started_line = last_line - count_of_lines + 1
        for line in inserted_file:
            current_line += 1
            if current_line >= started_line:
                last_num_lines.append(line)
    return last_num_lines


def get_intersection_of_lines(first_num_lines, last_num_lines):
    intersection = [line for line in first_num_lines if line in last_num_lines]
    return intersection


def get_args(argv=None):
    num_name = 'NUM'

    my_parser = argparse.ArgumentParser(description='Tool that help you analyze logs.', add_help=False)
    my_parser.add_argument('-h', '--help', action='help', help='Print help')
    my_parser.add_argument('-f', '--first', action='store', help=f'Print first {num_name} lines',
                           metavar=(num_name,))
    my_parser.add_argument('-l', '--last', action='store', help=f'Print last {num_name} lines',
                           metavar=(num_name,))
    my_parser.add_argument('-t', '--timestamps', action='store_true',
                           help='Print lines that contain a timestamp in HH:MM:SS format')
    my_parser.add_argument('-i', '--ipv4', action='store_true',
                           help='Print lines that contain an IPv4 address, matching IPs are highlighted')
    my_parser.add_argument('-I', '--ipv6', action='store_true',
                           help='Print lines that contain an IPv6 address (standard notation), matching IPs are '
                                'highlighted')
    my_parser.add_argument('inserted_file', action='store', nargs="?", type=argparse.FileType('r', encoding="utf-8", bufsize=-1),
                           help='Input file', default=sys.stdin, metavar=('FILE',))
    return my_parser.parse_args(argv)


def colored_line(dict_regex, dict_color, line):
    for key in dict_color:
        if key in dict_regex:
            line = re.sub(dict_regex[key], dict_color[key] + r'\1' + dict_color['end'], line)
    return line

def main():
    text_color = set_colors()
    re_ipv4, re_ipv6, re_timestamp = set_regex()
    searched_regex = {}

    # Get user intputs
    args = get_args()
    last_line = count_of_lines_in_file(args.inserted_file)


    #Find out which regular expressions searches should be performed
    with args.inserted_file as my_file:
        if args.ipv4:
            searched_regex['ipv4'] = re_ipv4

        if args.ipv6:
            searched_regex['ipv6'] = re_ipv6

        if args.timestamps:
            searched_regex['timestamps'] = re_timestamp

        #Analyze all linen
        my_file.seek(0)
        if not args.first and not args.last:
            for line in my_file:
                to_print = is_searched_pattern_in_line(searched_regex, line)  # get results of all regexp searches
                if all(to_print):  # if all analyzed regexp have been found, format and print given line
                    line = colored_line(searched_regex, text_color, line)
                    print(line, end='')
        else:
            if args.first and args.last:
                my_file.seek(0)
                first_num_lines = get_first_lines(my_file, int(args.first))
                my_file.seek(0)
                last_num_lines = get_last_lines(my_file, int(args.last), last_line)
                selected_lines = get_intersection_of_lines(first_num_lines, last_num_lines)


            elif args.first:

                selected_lines = get_first_lines(my_file, int(args.first))
            else:
                selected_lines = get_last_lines(args.inserted_file, int(args.last), last_line)


            for line in selected_lines:
                to_print = is_searched_pattern_in_line(searched_regex, line)
                if all(to_print):
                    print(colored_line(searched_regex, text_color, line))

if __name__ == '__main__':
    main()