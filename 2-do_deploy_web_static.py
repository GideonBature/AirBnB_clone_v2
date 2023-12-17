#!/usr/bin/python3
"""script that is based on the file `1-pack_web_static.py`
that distributes an archive to web servers using `do_deploy`
function.
"""
from fabric.api import *
from datetime import datetime
import os
from os.path import exists

env.hosts = ['204.236.240.142', '100.25.211.87']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """function that generates a .tgz archive from the contents
    of the `web_static` folder of your AirBnB Clone repo

    Return: None (failure) or archive path (success)
    """
    local("mkdir -p versions")

    t = datetime.now()
    t_str = t.strftime("%Y%m%d%H%M%S")

    archive_name = "web_static_{}".format(t_str)
    archive_path = "versions/{}".format(archive_name)

    # local(f"tar -cvzf {archive_path}.tgz web_static")

    if local(f"tar -cvzf {archive_path}.tgz web_static").succeeded:
        pkg_name = f"{archive_path}.tgz"
        archive_size = os.path.getsize(pkg_name)
        print(f"web_static packed: {archive_path}.tgz -> {archive_size}Bytes")
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to web servers

    @args:
        archive_path: path to the archive
    Returns: True(success) or False(Failure)
    """
    if not exists(archive_path):
        return False

    try:
        archive = archive_path.split('/')
        f = archive[1]
        fn = f.split('.')[0]

        put(archive_path, '/tmp/')

        run(f'sudo mkdir -p /data/web_static/releases/{fn}/')

        run(f'sudo tar -xzf /tmp/{f} -C /data/web_static/releases/{fn}/')

        run(f'sudo rm /tmp/{f}')

        run(f'sudo mv /data/web_static/releases/{fn}/web_static/* \
                /data/web_static/releases/{fn}/')

        run(f'sudo rm -rf /data/web_static/releases/{fn}/web_static')

        run('sudo rm -rf /data/web_static/current')

        run(f'sudo ln -s /data/web_static/releases/{fn}/ \
                /data/web_static/current')

        print('New version deployed!')

    except Exception:
        return False

    return True
