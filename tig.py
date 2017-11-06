import argparse
import glob
import os
import time
import random
import shutil
from distutils.dir_util import copy_tree

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

BACKUP_FOLDER_NAMES = ['old', 'oooold', 'old-old', 'very-old', 'old1', 'old2', 'olddddd', 'old11111', 'last', 'very-last']

def check_repo_exists_decorator(f): 
    def wrapper(*args, **kwargs): 
        if repo_exists():
            return f(*args, **kwargs)
        print "No repo found here. You should launch init first"
        return
    return wrapper 


def repo_exists():
    """ Check if a repo already exists """

    return os.path.exists('.tig')

def get_current_branch():
    """ Get the current branch name """

    _file = open(".tig/current_branch", "r")
    branch = _file.readline()
    _file.close()
    return branch


def get_last_backup():
    branch = get_current_branch()
    commits = ['.tig/branches/' + branch + '/' + d for d in os.listdir('.tig/branches/' + branch) if os.path.isdir('.tig/branches/' + branch + '/' + d)]
    return max(commits, key=os.path.getmtime)


def get_backup_name():
    """ Generate a backup folder name """
    
    return str(time.time()) + "_" + random.choice(BACKUP_FOLDER_NAMES)

def init():
    """ Init a new repo """

    if not repo_exists():
        os.makedirs('.tig')
        os.makedirs('.tig/branches/master')
        os.makedirs('.tig/tmp')

        _file = open(".tig/current_branch", "w")
        _file.write("master")
        _file.close()

        print "A new repository has been created! Ehm... not a real repo."
    else:
        print "Again? You already called init here, man!"


@check_repo_exists_decorator
def status():
    """ Print the repo status """

    print "Current branch is: " + get_current_branch()
    print "Last commit: " + get_last_backup()


@check_repo_exists_decorator
def commit():
    """ crea un backup """

    branch = get_current_branch()
    shutil.copytree('.', '.tig/branches/' + branch + '/' + get_backup_name(), ignore=shutil.ignore_patterns('.tig', 'tig.py'))
    print "Commit " + branch + '/' + get_backup_name() + " created."


@check_repo_exists_decorator
def pull():
    ''' non fa niente '''
    raise NotImplementedError("To be implemented")

def push():
    ''' crea zip? '''
    raise NotImplementedError("To be implemented")

def merge():
    print "You're f*cked, man. You're really f*cked"

def blame():
    print "So, you don't use a serious csv and you want to blame someone? Really?"

def rollback():
    ''' restore ultimo backup '''

    # save not versioned files to temp
        
    # empty current folder (not tig.py)
    files = os.listdir('.')
    for _f in files:
        if _f != '.tig' and _f != 'tig.py':
            if os.path.isdir(_f):
                shutil.rmtree(_f)
            else:
                os.remove(_f)
    # rollback
    backup_dir = get_last_backup()
    files = os.listdir(backup_dir)
    for _f in files:
        if _f != '.tig' and _f != 'tig.py':
            print _f
            if os.path.isdir(backup_dir + "/" + _f):
                shutil.copytree(backup_dir + "/" + _f, '.')
            else:
                shutil.copy(backup_dir + "/" + _f, '.')
    # restore not versione file from temp
    #last_backup = get_last_backup()
    #copy_tree(last_backup, '.')

    print "rollback from " + backup_dir

def branch(branch_name):
    ''' crea nuova cartella? '''
    raise NotImplementedError("To be implemented")

def help():
    raise NotImplementedError("To be implemented")

def main():
    print "Welcome to tig\n"
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?')
    args = parser.parse_args()

    if not args.command:
        help()
    else:
        try:
            if args.command not in AVAILABLE_COMMANDS:
                print "Command '" + args.command + "' not found. Available commands are: " + ", ".join(cmd for cmd in AVAILABLE_COMMANDS) + "."
            else:
                globals()[args.command]()
        except Exception as e:
            print e

if __name__ == "__main__":
    main()