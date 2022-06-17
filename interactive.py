import time
from helpers import *


class Interactive:
    stupid_people = 0
    noodle_heads = 0
    lost_it = False
    # configurator_info = '''
    #             Configurations
    #     --------------------------------------
    #         Domain: {domain}   IP: {ip}
    #         API KEY: {api}
    #         Degugging: {debug}
    #         Report: {report}
    #     --------------------------------------'''
    hackertarget_menu = """
           \t\t-----------------------
           \t\tHACKERTARGET TOOLS MENU
           \t\t-----------------------
\t[1] Traceroute        [9] IP Location Lookup        [m] Show this Menu                    
\t[2] Ping Test         [10] Reverse IP Lookup        [h] Set new host                      
\t[3] DNS Lookup        [11] TCP Port Scan            [a] Configure HackerTarget API        
\t[4] Reverse DNS       [12] Subnet Lookup            [d] Turn Debugging on or off          
\t[5] Find DNS Host     [13] HTTP Header Check        [i] Config Info
\t[6] Find Shared DNS   [14] Extract Page Links       [v] Version Info
\t[7] Zone Transfer     [15] ASN Lookup               [c] Clear Screen
\t[8] Whois Lookup                                    [l] Logo
\t                                                    [n] Check Network Status
\t                                                    [q] Exit
"""

    def __init__(self, hackertarget_api):
        self.hackertarget_api = hackertarget_api
        self.print_menu()

    def print_configurator_info(self):
        self.hackertarget_api.configurator.print_config()
        # print(self.configurator_info.format(domain=self.hackertarget_api.configurator.domain,
        #                                     ip=self.hackertarget_api.configurator.ip,
        #                                     api=self.hackertarget_api.configurator.hackertarget_api_key,
        #                                     debug=self.hackertarget_api.configurator.DEBUG,
        #                                     report=f'{self.hackertarget_api.configurator.report.file}.'
        #                                            f'{self.hackertarget_api.configurator.report.file_format}'))

    def print_menu(self):
        os.system(self.hackertarget_api.configurator.cmd)
        clear_screen()
        self.print_logo()
        print(self.hackertarget_menu)
        self.print_configurator_info()

    def print_version(self):
        clear_screen()
        print(self.hackertarget_api.configurator.hackertarget_logo)
        print(f'\t\t\t{self.hackertarget_api.configurator.version}')

    def print_logo(self):
        print(self.hackertarget_api.configurator.hackertarget_logo)

    def handle_debugging(self):
        if self.hackertarget_api.configurator.DEBUG:
            self.hackertarget_api.configurator.setup_debugging(option=False)
        else:
            self.hackertarget_api.configurator.setup_debugging(True)

    def handle_host(self):
        host = input('Enter new Host:\t\t')
        self.hackertarget_api.configurator.setup_host(host=host)
        self.print_configurator_info()

    def handle_api_key(self):
        print(f'API KEY: {self.hackertarget_api.configurator.hackertarget_api_key}')
        while True:
            if self.hackertarget_api.configurator.hackertarget_api_key:
                api_choice = input('Replace[re]|[e] or Remove[r] the existing API Key?\n(Press[b] to go back '
                                   'anytime)\t\t')
            else:
                api_choice = 'e'

            if api_choice == 'b':
                break
            elif api_choice == 'r':
                print('[!] Removing API Key...')
                if self.hackertarget_api.configurator.hackertarget_api_key:
                    self.hackertarget_api.configurator.setup_api_key('')
                else:
                    print('[!] API Key not Installed.')
                    break
            elif api_choice == 'e' or api_choice == 're':
                api_key = input('Type a New API Key. ')
                if api_key:
                    self.hackertarget_api.configurator.setup_api_key(api_key=api_key)
            else:
                print('Invalid Choice.')
                continue
            self.print_configurator_info()
            break

    # def handle_report_file(self):
    #     file = input('Enter File Path:\t\t')
    #     self.hackertarget_api.configurator.setup_report_file(file=file)
    #     self.print_configurator_info()
    #
    # def handle_report_format(self):
    #     file_format = input('Enter Format [txt|html|pdf]:\t\t')
    #     self.hackertarget_api.configurator.setup_report_file(file_format=file_format)
    #     self.print_configurator_info()

    def run_tool(self, tool_number):
        # clear_screen()
        tool = self.hackertarget_api.configurator.available_tools[tool_number - 1]
        if tool in self.hackertarget_api.configurator.strict_ip_query_tools:
            self.hackertarget_api.run(tool, self.hackertarget_api.configurator.ip)
        else:
            self.hackertarget_api.run(tool, self.hackertarget_api.configurator.domain)

    def run(self):
        stupidity_timeout = 3
        stupidity_counter = stupidity_timeout
        noodlehead_timeout = 2
        noodlehead_counter = noodlehead_timeout
        while True:
            try:
                if self.lost_it > 1:
                    print('\nValar Morghulis.')
                    break
                if self.noodle_heads >= noodlehead_timeout:
                    if noodlehead_timeout == noodlehead_counter:
                        print('You total numbnut. The hell u doing?')
                        print('You will get clearance in 10 seconds')
                        time.sleep(1)
                    self.lost_it += 1
                    noodlehead_timeout -= 1
                    self.noodle_heads -= 0

                if self.stupid_people >= stupidity_timeout:
                    if stupidity_timeout == stupidity_counter:
                        print('You lost your mind or something? Wait 5 seconds now.')
                        time.sleep(1)
                    self.noodle_heads += 1
                    self.stupid_people = 0
                    stupidity_timeout -= 1

                choice = input('\nChoose Your Option?\n(Press [m] for menu)\t')
                print('\n')

                if choice == '':
                    self.stupid_people += 1
                    continue
                if choice == 'h':
                    self.handle_host()
                elif choice == 'c':
                    clear_screen()
                elif choice == 'a':
                    self.handle_api_key()
                elif choice == 'd':
                    self.handle_debugging()
                elif choice == 'm':
                    self.print_menu()
                elif choice == 'v':
                    self.print_version()
                elif choice == 'i':
                    self.print_configurator_info()
                elif choice == 'l':
                    self.print_logo()
                elif choice == 'n':
                    if network_is_online():
                        print('[!] Network is UP.')
                    else:
                        print('[!] Network is DOWN !!')
                # elif choice == 'f':
                #     self.handle_report_file()
                elif choice == 'q':
                    break
                elif choice.isdigit() and 1 <= int(choice) <= 15:
                    if not self.hackertarget_api.configurator.domain and not self.hackertarget_api.configurator.ip:
                        self.handle_host()
                    self.run_tool(int(choice))

                else:
                    print(f'[!] Didn\'t recognize this option - {choice}')
                    self.stupid_people += 1

            except KeyboardInterrupt:
                print("Aborted!")
                break
