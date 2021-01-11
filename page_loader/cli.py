import os
import argparse


def take_apart_params():
    version = '0.1.0'
    parser = argparse.ArgumentParser(
        prog='page-loader',
        usage='page-loader [options] <url>',
        description='some description',
        add_help=False,
    )
    parser.add_argument('url', type=str)
    option_group = parser.add_argument_group(title='Options')
    option_group.add_argument(
        '-V',
        '--version',
        action='version',
        help='output the version number',
        version=f'{parser.prog} {version}',
    )
    option_group.add_argument(
        '-o',
        '--output',
        metavar='[dir]',
        type=str,
        default=os.getcwd() + os.sep + 'app',
        help='output dir (defoult: "/app")',
    )
    option_group.add_argument(
        '-h',
        '--help',
        action='help',
        help='display help for command'
    )
    return parser.parse_args()
