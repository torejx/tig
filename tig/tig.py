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

IGNORE_FILES = [
    'tig.py',
    '.tig',
    '.git',
    '.gitignore'
]

IGNORE_PATTERNS = [
    'tig.py',
    '.*'
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

def set_current_branch(branch_name):

    _file = open(".tig/current_branch", "w")
    _file.write(branch_name)
    _file.close()


def get_last_backup():
    branch = get_current_branch()
    commits = ['.tig/branches/' + branch + '/' + d for d in os.listdir('.tig/branches/' + branch) if os.path.isdir('.tig/branches/' + branch + '/' + d)]
    if not commits:
        return max(commits, key=os.path.getmtime)
    return None


def get_backup_name():
    """ Generate a backup folder name """
    
    return str(time.time()) + "_" + random.choice(BACKUP_FOLDER_NAMES)

def init():
    """ Init a new repo """

    if not repo_exists():
        os.makedirs('.tig')
        os.makedirs('.tig/branches/master')
        os.makedirs('.tig/tmp')

        set_current_branch('master')

        print "A new repository has been created! Ehm... not a real repo."
        return True
    else:
        print "Again? You already called init here, man!"
        return False


@check_repo_exists_decorator
def status():
    """ Print the repo status """
    
    last_backup = get_last_backup()

    print "Current branch is: " + get_current_branch()

    if last_backup:
        print "Last commit: " + get_last_backup()


@check_repo_exists_decorator
def commit():
    """ crea un backup """

    commit_dir = get_current_branch() + '/' + get_backup_name()
    shutil.copytree('.', '.tig/branches/' + commit_dir, ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

    # update mtime because copytree use copystats
    os.utime('.tig/branches/' + commit_dir, None)
    print "Commit " + commit_dir + " created."


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

    backup_dir = get_last_backup()
    if not backup_dir:
        print "Nothing to rollback to"
        return
        
    # empty current folder (not tig.py)
    files = os.listdir('.')
    for _f in files:
        if _f not in IGNORE_FILES:
            if os.path.isdir(_f):
                shutil.rmtree(_f)
            else:
                os.remove(_f)
    # rollback
    files = os.listdir(backup_dir)
    for _f in files:
        if _f not in IGNORE_FILES:
            if os.path.isdir(backup_dir + "/" + _f):
                shutil.copytree(backup_dir + "/" + _f, '.')
            else:
                shutil.copy(backup_dir + "/" + _f, '.')
    # restore not versione file from temp
    #last_backup = get_last_backup()
    #copy_tree(last_backup, '.')

    print "Rollback from " + backup_dir

def branch(branch_name):
    ''' crea nuova cartella? '''
    set_current_branch(branch_name)
    if not os.path.exists('.tig/branches/'+branch_name):
        os.makedirs('.tig/branches/'+branch_name)
    print "Switched to branch " + branch_name

def help():
    print "Welcome to TiG help\n"
    print "List of available commands: \n"
    print "tig.py init     \t\t init a new repository"
    print "tig.py status   \t\t check the repository status"
    print "tig.py commit   \t\t commit all files and directories"
    print "tig.py merge    \t\t perform a merge (maybe...)"
    print "tig.py push     \t\t push your commits (maybe...)"
    print "tig.py branch   \t\t create a new branch"
    print "tig.py blame    \t\t blame someone!"
    print "tig.py rollback \t\t revert your modification"
    print "tig.py help     \t\t display this help page"


def main():
    print "Welcome to TiG\n"
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?')
    parser.add_argument('param', nargs='?')
    args = parser.parse_args()

    if not args.command:
        help()
    else:
        try:
            if args.command not in AVAILABLE_COMMANDS:
                print "Command '" + args.command + "' not found. Available commands are: " + ", ".join(cmd for cmd in AVAILABLE_COMMANDS) + "."
            else:
                if args.command == 'branch':
                    if not args.param:
                        print "Insert branch name"
                    else:
                        globals()[args.command](args.param)        
                else:
                    globals()[args.command]()
        except Exception as e:
            print e

if __name__ == "__main__":
    main()