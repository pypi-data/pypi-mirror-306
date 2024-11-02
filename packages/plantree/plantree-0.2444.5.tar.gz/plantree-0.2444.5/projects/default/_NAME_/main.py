def main(*args):
    print(f"\nmain({', '.join(args)})\n")
    return True


if __name__ == '__main__':
    from sys import argv
    main(*argv[1:])
