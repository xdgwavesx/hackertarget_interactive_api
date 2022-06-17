import argparse
from configapi import ConfigAPI
from hackertargetapi import HackerTargetAPI

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'host',
        nargs='?',
        help='The domain to scan'
    )

    parser.add_argument(
        '--tools', required=False,
        help=f'Which hackertarget IP tool to run {ConfigAPI.available_tools}. Type a comma-separated list'
    )

    parser.add_argument(
        '--hackertarget-api-key',
        help='Can also be defined using the HACKERTARGET_API_KEY environment variable',
        dest='hackertarget_api_key', default=None
    )

    parser.add_argument(
        '-i', '--interactive',
        help='Run the script interactively',
        action='store_true',
        dest='interactive'
    )

    parser.add_argument(
        '-d', '--debugging',
        action='store_true',
        dest='debugging'
    )

    parser.add_argument(
        '-f', '--file',
        dest='file', metavar='<FILENAME>',
        default=None,
        help='Name and Location to store report'
    )

    parser.add_argument(
        '-o', '--file-format',
        dest='file_format', metavar='<FILE FORMAT>',
        help='Format for the report [html, pdf, txt]'
    )

    args = parser.parse_args()
    configurator = ConfigAPI(args)
    api = HackerTargetAPI(configurator)
    api.interact()
