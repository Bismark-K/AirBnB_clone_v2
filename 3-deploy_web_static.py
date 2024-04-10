#!/usr/bin/python3
"""
Create and distributes an archive to web servers
Author: Bismark-K
"""
import os.path
import time
from fabric.api import local
from fabric.operations import env, put, run

env.hosts = ['100.24.74.244', '100.26.225.2']


def do_pack():
    """Generate an tgz archive from web_static folder"""
    try:
        if isdir("versions") is False:
            local("mkdir versions")
        timestamp = time.strftime("%Y%m%d%H%M%S")
        archived_folder = f"versions/web_static_{timestamp}.tgz web_static/"
        local(f"tar -cvzf {archived_folder}.tgz web_static/")

        return archived_folder

    except Exception as e:
        print(f"Error: {e}")
        return None


def do_deploy(archive_path):
    """Send the archive to the web servers"""
    if (os.path.isfile(archive_path) is False):
        return False

    try:
        file = archive_path.split("/")[-1]
        folder = ("/data/web_static/releases/" + file.split(".")[0])
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(folder))
        run("tar -xzf /tmp/{} -C {}".format(file, folder))
        run("rm /tmp/{}".format(file))
        run("mv {}/web_static/* {}/".format(folder, folder))
        run("rm -rf {}/web_static".format(folder))
        run('rm -rf /data/web_static/current')
        run("ln -s {} /data/web_static/current".format(folder))
        print("Deployment done")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def deploy():
    """Make and send archive to the web servers"""
    try:
        path = do_pack()
        return do_deploy(path)

    except Exception as e:
        print(f"Error: {e}")
        return False
