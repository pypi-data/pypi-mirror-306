from sys import argv

from ..utils.console import print_version

if len(arg := argv[1:]) == 1 and arg[0] in {"-v", "--version"}:
    print_version()
    exit()  # early exit
