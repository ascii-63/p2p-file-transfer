# P2P Server

import os
import sys
import json
import socket


def getFilesInDir(_dir_path):
    """
    Get all files in a directory
    """
    files = [f for f in os.listdir(_dir_path) if os.path.isfile(
        os.path.join(_dir_path, f))]
    return files


if __name__ == "__main__":
    pass