#!/usr/bin/env python3
"""Fabric file used to run operations
locally(on the machine) and remotely(on the server)
"""
from fabric import Connection, task

@task
def send_file(c):
    result = c.put('0-setup_web_static.sh', '/home/ubuntu/')
    print("Uploaded {0.local} to {0.remote}".format(result))
