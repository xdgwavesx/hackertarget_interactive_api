import re
import time
from helpers import *
import sys

from report import Report


class ConfigAPI:
    DEBUG = False
    TRACE = False
    cmd = 'mode 120,35'
    version = 'v1.0.0 stable'
    configurator_info = '''       
                    Configurations 
            --------------------------------------
                Domain: {domain}   IP: {ip}
                API KEY: {api}           
                Debugging: {debug}
                Report: {report}               
            --------------------------------------'''
    hackertarget_logo = """
          _               _              _                          _
         | |_   __ _  __ | |__ ___  _ _ | |_  __ _  _ _  __ _  ___ | |_
         | ' \ / _` |/ _|| / // -_)| '_||  _|/ _` || '_|/ _` |/ -_)|  _|
         |_||_|\__,_|\__||_\_\\___||_|   \__|\__,_||_|  \__, |\___| \__|
                                                        |___/
                         |Nullwaves|"""
    available_tools = ['mtr', 'nping', 'dnslookup', 'reversedns',
                       'hostsearch', 'findsharedns', 'zonetransfer',
                       'whois', 'geoip', 'reverseiplookup', 'nmap',
                       'subnetcalc', 'httpheaders', 'pagelinks', 'aslookup']
    strict_ip_query_tools = ['reversedns', 'subnetcalc', 'aslookup']
    hackertarget_api_key = None
    interactive = False
    domain = None
    ip = None
    USER_AGENTS = [
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/57.0.2987.110 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.79 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
         'Gecko/20100101 '
         'Firefox/55.0'),  # firefox
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/61.0.3163.91 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/62.0.3202.89 '
         'Safari/537.36'),  # chrome
        ('Mozilla/5.0 (X11; Linux x86_64) '
         'AppleWebKit/537.36 (KHTML, like Gecko) '
         'Chrome/63.0.3239.108 '
         'Safari/537.36'),  # chrome
    ]

    def __init__(self, args):
        self.export_report = None
        self.report = None
        self.tools = None
        self.args = args
        self.parse()
        self.ALL_SET = True

    def parse(self):
        self.setup_debugging()
        self.print_debug('Configuring HackerTarget API')
        self.setup_api_key()

        if not self.args.interactive:
            if not self.args.host:
                print('[!] Please specify a host.\n')
                sys.exit(1)

            if not self.args.tools:
                print(
                    '[!] You are not running in Interactive Mode. Please specify tools to run with --tools '
                    '<tool_name> in a comma-separated list.\n')
                sys.exit(1)

            self.setup_host()
            self.setup_tools()
        else:
            self.setup_interactive()
        self.setup_report_file()
        # self.setup_proxy()
        self.print_debug('-> Alright we are good to go ->\n')
        return self

    def setup_debugging(self, option=False):
        if self.args.debugging:
            self.DEBUG = True
        else:
            self.DEBUG = option
        self.print_debug(f'[!] Debugging => {self.DEBUG}\n')

    def print_debug(self, *args):
        if self.DEBUG:
            print('[!]', end=' ')
            print(*args)


    def setup_api_key(self, api_key=None):

        self.print_debug('Setting Up Hackertarget API Key')

        if api_key is not None:
            self.hackertarget_api_key = api_key
        elif self.args.hackertarget_api_key:
            self.hackertarget_api_key = self.args.hackertarget_api_key
        elif 'HACKERTARGET_API_KEY' in os.environ:
            self.hackertarget_api_key = os.environ['HACKERTARGET_API_KEY']

        if not self.hackertarget_api_key:
            self.print_debug(
                '\t[+] No API Key set. Your requests will be limited according to Hackertarget terms.\n'
                '\t[+] You can set your Hackertarget API Key from your environment (HACKERTARGET_API_KEY) or from the '
                'command line (--hackertarget-api-key) or using the interactive menu.\n')
        # self.print_debug(f'[+] API Key: {self.hackertarget_api_key}\n')
        return self

    @staticmethod
    def domain_to_ip(domain):
        return socket.gethostbyname(domain)

    @staticmethod
    def ip_to_domain(ip):
        return socket.gethostbyaddr(ip)

    def setup_host(self, host=None):

        print('[!] Configuring Host')
        domain_pattern = '(//|\s+|^)(\w\.|\w[A-Za-z0-9-]{0,61}\w\.){1,3}[A-Za-z]{2,6}'
        valid_domain = re.compile(domain_pattern)

        ip_pattern = '^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$'
        valid_ip = re.compile(ip_pattern)

        if host is None:
            host = self.args.host

        retries = 3
        i = 0
        chances = 0
        while i <= retries:
            try:
                if re.match(valid_domain, host):
                    domain = host
                    self.print_debug(f'\t[+] Computing IP Address from {domain}....')
                    ip = ConfigAPI.domain_to_ip(host)

                elif re.match(valid_ip, host):
                    ip = host
                    self.print_debug(f'\t[+] Computing Domain name from {ip}....')
                    domain = ConfigAPI.ip_to_domain(host)[0]
                else:
                    sys.stderr.write('[!!] Not a valid Domain or IP Address. Aborting....\n')
                    break
                self.print_debug(f'\t[+] Domain name: {domain}')
                self.print_debug(f'\t[+] IP Address: {ip}\n')
                self.domain = domain
                self.ip = ip
                if self.report:
                    self.report.heading_written = False
                break
            except socket.herror as sock_host_err:
                self.print_debug('Host Error: ', sock_host_err)
            except socket.gaierror as sock_address_info_err:
                self.print_debug('Address Info Error: ', sock_address_info_err)
            except socket.timeout as sock_timeout_err:
                self.print_debug('Timeout Error: ', sock_timeout_err)
            except Exception as err:
                self.print_debug('Unknown Error: ', err)
                # traceback.print_exc()
            i += 1
            if chances >= 1:
                print('\n[!] unknown error occurred while setting up host. quitting now...')
                quit()
            else:
                print('Retrying again in 5 seconds.....\n')
                time.sleep(5)
                if i >= retries:
                    print('[!] Can\'t resolve domain and ip address. Checking network connection...\n')
                    if network_is_online():
                        print('[!] Network is online. Trying setting up domain and ip again\n')
                        i = 0
                        retries = 2
                        chances += 1
                        continue
                    else:
                        print('[!] Network is dead. Goodbye')
                        quit()
        return self

    def setup_tools(self):
        self.print_debug('Configuring tools to run....')
        tools = self.args.tools

        tools += ','
        valid_tools = []
        tools = tools.split(',')
        for tool in tools:
            if tool == 'all':
                valid_tools = self.available_tools
                break
            if tool == '':
                continue
            if tool not in self.available_tools:
                sys.stderr.write(
                    f'[!] Invalid Tool name {tool}. Please verify with Hackertarget IP Toolset. Skipping...')
                continue
            valid_tools.append(tool)
        self.print_debug(f'Tools we are gonna run: {[tool.upper() for tool in valid_tools]}\n')
        self.tools = valid_tools
        return self

    def setup_interactive(self):
        self.interactive = True
        if self.args.host:
            self.setup_host()
        else:
            self.print_debug('No host specified.\n')

    def setup_report_file(self, file=None, file_format='txt'):
        if not file:
            if self.args.file:
                file = self.args.file
        if self.args.file_format:
            file_format = self.args.file_format
        self.report = Report(file=file, file_format=file_format, configurator=self)

    def print_config(self, return_string=False):
        if self.ALL_SET:
            config = self.configurator_info.format(domain=self.domain,
                                                   ip=self.ip,
                                                   api=self.hackertarget_api_key,
                                                   debug=self.DEBUG,
                                                   report=f'{self.report.file if self.report.file else None}'
                                                          f'{"." if self.report.file else ""}'
                                                          f'{self.report.file_format if self.report.file_format else ""}')
            if not return_string:
                print(config)
            else:
                return config
