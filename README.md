# hackertarget_interactive_api
HackerTarget API's through command line interactive interface or can be automated through command line


## Usage
usage: main.py [-h]

               [--tools TOOLS] [--hackertarget-api-key HACKERTARGET_API_KEY] [-i] [-d]
               [-f <FILENAME>]
               [-o <FILE FORMAT>]
               [host]

#### positional arguments:
  
  **host**    -    The domain to scan (default: None)

#### optional arguments:
  
  **-h, --help**            show this help message and exit
  
  **--tools TOOLS**      hackertarget IP tool to run ['mtr', 'nping', 'dnslookup', 'reversedns', 'hostsearch',
                        'findsharedns', 'zonetransfer', 'whois', 'geoip', 'reverseiplookup', 'nmap', 'subnetcalc',
                        'httpheaders', 'pagelinks', 'aslookup'].
                        Type a comma-separated list (default: None)
  
  **--hackertarget-api-key HACKERTARGET_API_KEY** 
                        Can also be defined using the HACKERTARGET_API_KEY environment variable (default: None)
  
  **-i, --interactive**     Run the script interactively (default: False)
  
  **-d, --debugging**
  
  **-f <FILENAME>, --file <FILENAME>**   Name and Location to store report (default: None)
  
  **-o <FILE FORMAT>, --file-format <FILE FORMAT>**
  Format for the report [html, pdf, txt] (default: None)



## Screenshots
    
![hackertarget](hackertarget_api.png?raw=true "HackerTarget Interactive API"):
