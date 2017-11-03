import argparse
import os
import time
import random
from shutil import copytree, ignore_patterns

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

def get_backup_name():
    """ Generate a backup folder name """
    
    return str(time.time()) + "_" + random.choice(BACKUP_FOLDER_NAMES)

def init():
    """ Init a new repo """

    if not repo_exists():
        os.makedirs('.tig')
        os.makedirs('.tig/branches/master')

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


@check_repo_exists_decorator
def commit():
    """ crea un backup """

    branch = get_current_branch()
    copytree('.', '.tig/branches/' + branch + '/' + get_backup_name(), ignore=ignore_patterns('*.pyc', '.*', 'tig.py'))
    print "Commit ok! Yeah..."


@check_repo_exists_decorator
def pull():
    ''' non fa niente '''
    print "pull"

def push():
    ''' crea zip? '''
    print "push"

def merge():
    print "You're f*cked, man. You're really f*cked"

def blame():
    print "So, you don't use a serious csv and you want to blame someone? Really?"

def rollback():
    ''' restore ultimo backup '''
    print "rollback"

def branch(branch_name):
    ''' crea nuova cartella? '''
    print "branch"

def help():
    print "HELP"

def main():
    print "Welcome to tig"
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