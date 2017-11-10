import argparse
import glob
import os
import time
import random
import shutil
from distutils.dir_util import copy_tree

ROOT = '.tig'
BRANCHES_FOLDER = os.path.join(ROOT, 'branches')
TMP_FOLDER = os.path.join(ROOT, 'tmp')
CURRENT_BRANCH_PATH = os.path.join(ROOT, 'current_branch')
DEFAULT_BRANCH = 'master'
AVAILABLE_COMMANDS = [
    'init',
    'commit',
    'branch',
    'pull',
    'push',
    'merge',
    'blame',
    'rollback',
    'help',
    'status'
    ]

IGNORE_FILES = [
    'env',
    'venv',
    'tig.py',
    '.tig',
    '.git',
    '.gitignore'
]

IGNORE_PATTERNS = [
    'tig.py',
    '.*',
    'env',
    'venv'
]

BACKUP_FOLDER_NAMES = [
    'old',
    'oooold',
    'old-old',
    'very-old',
    'old1',
    'old2',
    'olddddd',
    'old11111',
    'last',
    'very-last'
]

def check_repo_exists_decorator(f): 
    def wrapper(*args, **kwargs): 
        if repo_exists():
            return f(*args, **kwargs)
        print "No repo found here. You should launch init first"
        return
    return wrapper 


def repo_exists():
    """ Check if a repo already exists """

    return os.path.exists(ROOT)

def get_current_branch():
    """ Get the current branch name """

    _file = open(CURRENT_BRANCH_PATH, "r")
    branch = _file.readline()
    _file.close()
    return branch

def set_current_branch(branch_name):
    """ Set the current branch name """

    _file = open(CURRENT_BRANCH_PATH, "w")
    _file.write(branch_name)
    _file.close()


def get_last_backup():
    """ Get the most recent backup folder """

    branch = get_current_branch()
    commits = [os.path.join(BRANCHES_FOLDER, branch, d) for d in os.listdir(os.path.join(BRANCHES_FOLDER, branch)) if os.path.isdir(os.path.join(BRANCHES_FOLDER, branch, d))]
    if commits:
        return max(commits, key=os.path.getmtime)
    return None


def get_backup_name():
    """ Generate a backup folder name """
    
    return str(time.time()) + "_" + random.choice(BACKUP_FOLDER_NAMES)