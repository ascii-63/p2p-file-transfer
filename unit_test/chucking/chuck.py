import subprocess
import os
import sys


def chucking(_size, _file_path):
    """
    Chuck a file into numbers of _size (MB) file
    """

    file_size = str(_size) + 'M'
    ochuck_name = os.path.basename(_file_path) + '_'
    chuck_name = './chucks/' + ochuck_name

    try:
        result = subprocess.run(["split", "-a", "3", "-b", file_size, "-d",
                                _file_path, chuck_name], capture_output=True, text=True, check=True)
        print(f"split command output: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(
            f"spilt command failed with return code: {e.returncode} and output : {e.output}")


if __name__ == "__main__":
    chucking(50, sys.argv[1])
