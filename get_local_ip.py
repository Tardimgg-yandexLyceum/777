import subprocess
from sys import platform
import socket


def get_ip():
    if platform == 'linux' or platform == "linux2":
        res = subprocess.check_output("hostname -I", shell=True).split()[0]
        return "".join(list(map(lambda x: chr(x), res)))
    if platform == 'win32' or platform == 'win64':

        hostname = socket.gethostname() 
        IP = socket.gethostbyname(hostname) 
        return "".join(list(map(lambda x: chr(x), IP)))
