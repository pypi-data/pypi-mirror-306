from sys import argv

from ..utils.print_version import print_version

if "--version" in argv or "-v" in argv:
    print_version()
    exit()  # early exit
