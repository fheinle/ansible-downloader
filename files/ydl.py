#!/home/downloads/.venv/bin/python
# -*- coding: utf-8" -*-

""" small wrapper around youtube-dl to use with a proxy and only echo URIs """

import sys
import json
import urllib.request
import configparser
import io

import youtube_dl


def get_rpc_password(fname='/home/downloads/config/aria2.conf'):
    """get aria2s RPC password from its configuration file"""
    # aria2s configuration file is init without a section
    # we'll work around that by adding a dummy section to our input
    configuration = "[root]\n" + open(fname, 'r').read()
    configuration_fake_file = io.StringIO(configuration)
    config = configparser.RawConfigParser()
    config.readfp(configuration_fake_file)
    rpc_password = config.get('root', 'rpc-secret')
    return rpc_password


def get_filename_and_url(url):
    """get download url for given filehoster url"""
    ydl_opts = {'proxy': '127.0.0.1:8123'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(url, download=False)
    return ("%s.%s" % (result['title'],
                       result['ext']),
            result['url']
            )


def add_download(filename, url):
    """send download link and filename to aria over rpc"""
    json_request = json.dumps({'jsonrpc': '2.0',
                               'id':       'qwer',
                               'method':   'aria2.addUri',
                               'params': [
                                          r'token:' + get_rpc_password(),
                                          [url],
                                          {'out': filename},
                               ]
                               })
    request_result = urllib.request.urlopen(
        'http://127.0.0.1:6800/jsonrpc',
        bytes(json_request, encoding='utf-8')
    )
    return json.loads(request_result.read().decode('utf-8'))['result']

if __name__ == '__main__':
    filename, url = get_filename_and_url(sys.argv[1])
    print("Adding %s" % filename)
    add_download(filename, url)
