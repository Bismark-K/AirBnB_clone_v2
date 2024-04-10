#!/usr/bin/python3
"""
fabric script to generate a .tgz archive from the contents of the web_static
folder.
Author: Bismark-K
"""
import time
from fabric.api import local


def do_pack():
    """compress the web_static folder"""
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static/".
              format(time.strftime("%Y%m%d%H%M%S")))
        return ("versions/web_static_{}.tgz".format(time.
                                                    strftime("%Y%m%d%H%M%S")))
    except Exception:
        return None
