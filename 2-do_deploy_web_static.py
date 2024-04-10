#!/usr/bin/python3
"""
fabric script that sends a compressed folder to the web servers
Author: Bismark-K
"""

from datetime import datetime
from fabric.api import *
import os

env.hosts = ["100.26.225.2", "100.24.74.244"]
env.user = "ubuntu"


def do_pack():
    """
        return the archive path if archive has generated correctly.
    """

    local("mkdir -p versions")
    date = datetime.now().strftime("%Y%m%d%H%M%S")
    loc_archived_path = "versions/web_static_{}.tgz".format(date)
    zipped_archive = local("tar -cvzf {} web_static".format(loc_archived_path))

    if zipped_archive.succeeded:
        return loc_archived_path
    else:
        return None


def do_deploy(archive_path):
    """
        send archive to the servers.
    """
    if os.path.exists(archive_path):
        archived_file = archive_path[9:]
        newest_version = "/data/web_static/releases/" + archived_file[:-4]
        archived_file = "/tmp/" + archived_file
        put(archive_path, "/tmp/")
        run("sudo mkdir -p {}".format(newest_version))
        run("sudo tar -xzf {} -C {}/".format(archived_file,
                                             newest_version))
        run("sudo rm {}".format(archived_file))
        run("sudo mv {}/web_static/* {}".format(newest_version,
                                                newest_version))
        run("sudo rm -rf {}/web_static".format(newest_version))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(newest_version))

        print("You have successfully deployed a new version!")
        return True

    return False
