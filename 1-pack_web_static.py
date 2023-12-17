#!/usr/bin/python3
"""script that generates a .tgz archive from the contents
of the `web_static` folder of your AirBnB Clone repo,
using the function `do_pack`.
"""
from fabric.api import local
from datetime import datetime
import os


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
