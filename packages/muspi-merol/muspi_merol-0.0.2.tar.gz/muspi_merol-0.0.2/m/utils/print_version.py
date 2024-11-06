def print_version():
    from platform import python_implementation, python_version

    from rich import print

    from ..version import __version__

    print(f"\n [r] m [/r] {__version__} {python_implementation()} {python_version()}\n")
