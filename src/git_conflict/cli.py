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
    parser.add_argument('--install', dest='action', action='store_const',
                        const='install', help='install git conflict')
    parser.add_argument('--publish', dest='action', action='store_const',
                        const='publish', help='publish rr-cache to origin')
    # parser.add_argument('ref',
    #                     help=('Commit-ish object names to merge.\n'
    #                           'Defaults to HEAD if omitted.'),
    #                     metavar='commit-ish', nargs='?')
    args = parser.parse_args(args)
    return args, parser
