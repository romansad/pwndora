#!/usr/bin/env python
from Commands import Commands
from colorama import Fore
from loguru import logger
from datetime import datetime
from Ports import TOP_PORTS, COMMON_PORTS
from ThreadScanner import Thread_Scanner
import sys

__author__ = "Alejandro Chilczenko"
__copyright__ = "Copyright 2021, "
__credits__ = ["Alejandro Chilczenko"]
__license__ = "Apache 2.0"
__version__ = "1.0.2"
__email__ = "alechilczenko@gmail.com"
__status__ = "Development"

def show():
    return Fore.GREEN +'''

              ,---------------------------,
              |  /---------------------\  |
              | |                       | |
              | |     Computer          | |
              | |      Services         | |
              | |       Company         | |
              | |                       | |
              |  \_____________________/  |
              |___________________________|
            ,---\_____     []     _______/------,
          /         /______________\           /|
        /___________________________________ /  | ___
        |                                   |   |    )
        |  _ _ _                 [-------]  |   |   (
        |  o o o                 [-------]  |  /    _)_
        |__________________________________ |/     /  /
    /-------------------------------------/|      ( )/
  /-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/-/ /
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '''+ Fore.RESET

#Search country IP blocks in https://www.nirsoft.net/countryip{COUNTRY_CODE}.html
def get_country_ip_blocks(file):
    total = []
    with open(file, 'r') as flist:
        blocks = list(filter(None,flist.read().split('\n')))
    for ip in blocks:
        line = ip.split(",")
        block = [line[0],line[1]]
        total.append(block)
    return total

def massive_scan(path,threads,timeout,screenshot,top_ports,all_ports):
    #Scan total of ip blocks in file
    for ip in get_country_ip_blocks(path):
        start = ip[0]
        end = ip[1]
        Discover = Thread_Scanner(start, end, threads,timeout,screenshot)
        set_port_scan(Discover,top_ports,all_ports)
        Discover.start_threads()

def set_port_scan(Discover,top_ports,all_ports):
    if top_ports:
        Discover.set_ports(TOP_PORTS)
    elif all_ports:
        Discover.set_ports(COMMON_PORTS)

def main():
    print(show())
    start, end, threads, path, timeout, screenshot, top_ports, all_ports = Commands.get_flags()
    #Verify argument validity
    if  start and end:
        Discover = Thread_Scanner(start,end,threads,timeout,screenshot)
        set_port_scan(Discover,top_ports,all_ports)
        Discover.start_threads()

    elif path:
        start = datetime.now()
        massive_scan(path,threads,timeout,screenshot,top_ports,all_ports)
        end = datetime.now()
        elapsed = end-start
        logger.info("Total execution time: {}".format(elapsed))
    else:
        logger.info("Please use -h to see all options")
        sys.exit(1)
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("You pressed CRTL+C")
        sys.exit(1)