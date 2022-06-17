import random
import time
import requests
from configapi import ConfigAPI
from interactive import Interactive
from helpers import *


class HackerTargetAPI:

    def __init__(self, configurator: ConfigAPI):
        self.results = None
        self.configurator = configurator

    def interact(self):
        if self.configurator.interactive:
            self.interactive()
        else:
            self.non_interactive()

    def non_interactive(self):
        for tool in self.configurator.tools:
            if tool in self.configurator.strict_ip_query_tools:
                self.run(tool, self.configurator.ip)
            else:
                self.run(tool, self.configurator.domain)

    def interactive(self):
        api = Interactive(self)
        api.run()

    def run(self, tool=None, query=None):
        self.configurator.print_debug('Running the API NOW...\n')
        api_base = 'https://api.hackertarget.com/{tool}/?q={query}'
        if self.configurator.hackertarget_api_key is not None and self.configurator.hackertarget_api_key != '':
            api_base += f'&apikey={self.configurator.hackertarget_api_key}'

        url = api_base.format(tool=tool, query=query)
        print(f'\n[!] Running Tool - {tool.upper()}')
        self.configurator.print_debug(f'\t[+] Sending request to - {url}.')
        self.configurator.print_debug(f'\t[+] Waiting for Response...')

        retries = 5
        i = 0
        while i < retries:
            try:
                user_agent = random.choice(self.configurator.USER_AGENTS)
                headers = {'User-Agent': user_agent}
                response = requests.get(url, headers=headers, timeout=8.0)
                if self.configurator.TRACE:
                    print(f'\n{response.request.headers}\n')
                    # print(f'{proxy}\n')
                    print(f'{user_agent}\n')
                self.results = response
                self.prepare_report(tool=tool)
                print('\n')
                break

            except requests.exceptions.HTTPError as http_err:
                self.configurator.print_debug("Http Error:", http_err)
            except requests.exceptions.ConnectionError as conn_err:
                self.configurator.print_debug("Error Connecting:", conn_err)
            except requests.exceptions.Timeout as timeout_err:
                self.configurator.print_debug("Timeout Error:", timeout_err)
            except requests.exceptions.RequestException as err:
                self.configurator.print_debug("Can't figure out but an error surely occured", err)
                # traceback.print_exc()
            i += 1
            print('Retrying again in 5 seconds.....\n')
            time.sleep(5)
        else:
            print('Can\'t connect with the API. Please check your Network Connection. It\'s dead.')

    def prepare_report(self, tool):
        self.configurator.report.insert_data(self.results, tool=tool)
        self.configurator.report.print_report()
        if self.configurator.report.export:
            self.export_report()

    def export_report(self):
        self.configurator.report.export_report()
