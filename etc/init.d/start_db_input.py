#!/usr/bin/python
# -*- coding: utf-8 -*-
# Inspired by : http://gitorious.org/forban/forban/blobs/master/bin/forbanctl

"""
Start the service inserting the new entries in the Redis database
"""
import os
import sys
import ConfigParser

import signal
from pubsublogger import publisher
import argparse


if __name__ == '__main__':

    publisher.channel = 'DatabaseInput'

    parser = argparse.ArgumentParser(description='Start the database input processes')
    parser.add_argument('action', choices=('start', 'stop'))
    args = parser.parse_args()

    config = ConfigParser.RawConfigParser()
    config_file = "/etc/bgpranking/bgpranking.conf"
    config.read(config_file)
    root_dir = config.get('directories','root')
    sys.path.append(os.path.join(root_dir,config.get('directories','libraries')))
    from helpers.initscript import *
    services_dir = os.path.join(root_dir,config.get('directories','services'))

    service = os.path.join(services_dir, "db_input")

    if args.action == "start":
        print("Starting insertion...")
        publisher.info("Starting insertion...")
        print(service + " to start...")
        publisher.info(service + " to start...")
        service_start_multiple(servicename = service, number = \
                int(config.get('processes','input')))

    elif args.action == "stop":
        print("Stopping insertion...")
        publisher.info("Stopping insertion...")
        pids = pidof(processname=service)
        if pids:
            print(service + " to be stopped...")
            publisher.info(service + " to be stopped...")
            for pid in pids:
                try:
                    os.kill(int(pid), signal.SIGHUP)
                except OSError, e:
                    print(service + " unsuccessfully stopped")
                    publisher.error(service +  " unsuccessfully stopped")
            rmpid(processname=service)
