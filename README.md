# Ansible Downloader

installs aria2 as a downloader, supported by youtube-dl, tor and polipo

## Description

This installs a package of software for downloading from various sources on the
internet over tor. ``aria2`` is used for its queueing feature, ``youtube-dl`` is
used to extract download urls for files not directly accessible (e.g. youtube
videos), ``tor`` is used for general anonymization and ``polipo`` as the http
proxy supporting tor.

Additionaly, it comes with an RPC server that accepts new urls to download.

## Installation

Clone this repository to your ansible roles directory:

    mkdir roles/
    git clone git@github.com:fheinle/ansible-downloader.git roles/downloader

You can also optionally push the included ``files/aria2_1.20.0-1_armhf.deb`` to
your destination host and install it (has ``libc-ares2`` as a dependency) if
you're experiencing problems with HTTPS downloads.

## Usage

This role needs to be passed two variables:

    rpc_user: username
    rpc_password: password

for the remote control feature in the included rpc server for starting downloads.

## Build

[![Build Status](https://travis-ci.org/fheinle/ansible-downloader.svg?branch=master)](https://travis-ci.org/fheinle/ansible-downloader)

## Copyright

Copyright (c) 2016 Florian Heinle <launchpad@planet-tiax.de>

MIT License
