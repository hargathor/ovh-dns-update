#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : ovh-dns-auto-update.py
# Author            : hargathor <3949704+hargathor@users.noreply.github.com>
# Date              : 11.03.2019
# Last Modified Date: 11.03.2019
# Last Modified By  : hargathor <3949704+hargathor@users.noreply.github.com>

# -*- encoding: utf-8 -*-

import json
import logging
import logging.handlers
import time
from pprint import pprint

import dns.resolver
import ovh
from requests import get


def log_setup():
    log_handler = logging.handlers.WatchedFileHandler('/var/log/ovh.log')
    formatter = logging.Formatter(
        '%(asctime)s %(filename)s [%(process)d] %(levelname)s: %(message)s',
        '%b %d %H:%M:%S')
    formatter.converter = time.localtime
    log_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.addHandler(log_handler)
    logger.setLevel(logging.DEBUG)

def check_ip(domaine_name):
    """TODO: Docstring for check_ip.

    :a: TODO
    :returns: the ip of the domaine name

    """
    current_ip = get('https://api.ipify.org').text
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['8.8.8.8']
    answer = resolver.query(domaine_name)
    wanted_ip = answer[0]
    if str(current_ip) == str(wanted_ip):
        return True
    return False

def update_ip(a_field, ip, client):
    """ Update IP for the A field

    :a: TODO
    :ip: IP
    :client: OVH client
    :returns: TODO

    """
    logging.info("Updating {} to IP {}".format(a_field, ip))
    result = client.put('/domain/zone/domaineferrari.com/record/{}'.format(a_field['id']), 
            ttl=0, 
            subDomain=a_field['subDomain'],
            target=ip)

def refresh_domain(domaine, client):
    """TODO: Docstring for refresh_domain.

    :domaine: TODO
    :returns: TODO

    """
    result = client.post('/domain/zone/{}/refresh'.format(domaine))


def main():
    """TODO: Docstring for main.
    :returns: TODO

    """
    # By default it looks in ./ovh.conf, ~/.ovh.conf or /etc/ovh.conf
    # client = ovh.Client(config_file='/home/hargathor/dev/ovh-dns-auto-update/ovh.conf')
    client = ovh.Client()

    if not check_ip('domaineferrari.com'):
        ip = get('https://api.ipify.org').text
        result = client.get('/domain/zone/domaineferrari.com/record', fieldType='A')
        for field in result:
            domain_def = client.get('/domain/zone/domaineferrari.com/record/{}'.format(field))
            update_ip(domain_def, ip, client)
        refresh_domain('domaineferrari.com', client)


if __name__ == '__main__':
    log_setup()
    main()
