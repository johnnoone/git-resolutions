import argparse
import sys


class Parser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def parse_args(args=None):
    parser = Parser(prog='git conflict',
                    usage='%(prog)s --prepare | --publish | <commit-ish>',
                    description='publish merge resolutions')
    parser.set_defaults(action='noop')
    parser.add_argument('-i', '--install', dest='action', action='store_const',
                        const='install', help='install git conflict')
    parser.add_argument('-p', '--publish', dest='action', action='store_const',
                        const='publish', help='push resolutions to origin')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                        help='force command, even on mixmatch')
    parser.add_argument('--directory')
    parser.add_argument('ref',
                        help=('commit-ish object names to merge'),
                        metavar='commit-ish', nargs='?')
    args = parser.parse_args(args)
    return args, parser
