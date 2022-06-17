import requests, os


class Report:
    file = None
    file_format = 'txt'
    export = False
    fp = None
    data = None
    heading_written = False

    def __init__(self, file, file_format, configurator):
        self.file = file
        self.file_format = file_format
        self.configurator = configurator
        if self.file:
            self.export = True
            self.setup_file()
        else:
            self.file_format = None

    def setup_file(self):
        if os.path.exists(self.file + '.' + self.file_format):
            os.remove(self.file + '.' + self.file_format)
        self.fp = open(f'{self.file}.{self.file_format}', 'ab')

    def export_report(self):
        if self.fp:
            if not self.heading_written:
                self.fp.write(self.configurator.print_config(return_string=True).encode() + b'\n\n\n\n')
                self.heading_written = True

            if self.data:
                self.fp.write(b'-' * 50 + b'\n' + b'\t\t' + self.data[0].encode() + b'\n' + b'-' * 50 + b'\n\n')
                self.fp.write(b'\n\n'.join([self.data[1].content]))
                self.fp.write(b'\n\n\n\n')

    def insert_data(self, data: requests.Response, tool):
        self.data = (tool, data)

    def print_report(self):
        print(self.data[1].text)

    def print_config(self):
        print(f'{self.file}.{self.file_format}')

    def __exit__(self, *args):
        self.fp.close()

