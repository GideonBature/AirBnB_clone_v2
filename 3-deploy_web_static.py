#!/usr/bin/python3
"""script that is based on the file `1-pack_web_static.py`
that distributes an archive to web servers using `do_deploy`
function.
"""
from fabric.api import *
from datetime import datetime
import os
import os.path
from os.path import exists

env.hosts = ['204.236.240.142', '100.25.211.87']
# env.user = 'ubuntu'
# env.key_filename = '~/.ssh/school'


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

    archive = archive_path.split('/')
    f = archive[1]
    fn = f.split('.')[0]

    if put(archive_path, '/tmp/').failed:
        return False

    if run('sudo mkdir -p /data/web_static/releases/{}/'.format(fn)).failed:
        return False

    if run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(f, fn)).failed:
        return False

    if run('sudo rm /tmp/{}'.format(f)).failed:
        return False

    if run('sudo mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'.format(fn, fn)).failed:
        return False

    if run('sudo rm -rf /data/web_static/releases/{}/web_static'.format(fn)).failed:
        return False

    if run('sudo rm -rf /data/web_static/current').failed:
        return False

    if run('sudo ln -s /data/web_static/releases/{}/ \
            /data/web_static/current'.format(fn)).failed:
        return False

    print('New version deployed!')

    return True



def deploy():
    """creates and distributes an archive to
    your web servers
    """
    file = do_pack()

    if file is None:
        return False

    return do_deploy(file)

if __name__ == '__main__':
    deploy()
