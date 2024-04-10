#!/usr/bin/python3
"""
fabric script to generate a .tgz archive from the contents of the web_static
folder.
Author: Bismark-K
"""
import time
from fabric.api import local
from os.path import isdir


def do_pack():
    """compress the web_static folder"""
    try:
        timestamp = time.strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        archived_folder = f"versions/web_static_{timestamp}.tgz"
        local(f"tar -cvzf {archived_folder} web_static/")

        return archived_folder
    except Exception as e:
        print(f"Error: {e}")
        return None
