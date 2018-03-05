import argparse
import glob
import os
import time
import random
import shutil
from distutils.dir_util import copy_tree
from utils import *

def init():
    """ Init a new repo """

    if not repo_exists():
        os.makedirs(ROOT)
        os.makedirs(os.path.join(BRANCHES_FOLDER, DEFAULT_BRANCH))
        os.makedirs(TMP_FOLDER)

        set_current_branch(DEFAULT_BRANCH)

        print "A new repository has been created! Ehm... not a real repo."
        return True
    else:
        print "Again? You already called init here, man!"
        return False


@check_repo_exists_decorator
def status():
    """ Print the repo status """
    
    last_backup = get_last_backup()
    current_branch = get_current_branch()

    print "Current branch is: %s" % current_branch

    if last_backup:
        print "Last commit: %s" % last_backup.replace(BRANCHES_FOLDER + os.sep, '')


@check_repo_exists_decorator
def commit():
    """ Create a new commit """

    commit_dir = get_current_branch() + '/' + get_backup_name()
    commit_dir = os.path.join(get_current_branch(), get_backup_name())
    shutil.copytree('.', os.path.join(BRANCHES_FOLDER, commit_dir), ignore=shutil.ignore_patterns(*IGNORE_PATTERNS))

    # update mtime because copytree use copystats
    os.utime(os.path.join(BRANCHES_FOLDER, commit_dir), None)
    print "Commit %s created." % commit_dir


@check_repo_exists_decorator
def pull():
    ''' non fa niente '''
    raise NotImplementedError("To be implemented")

def push():
    ''' crea zip? '''
    raise NotImplementedError("To be implemented")

def log():
    """ Show history """
    raise NotImplementedError("To be implemented")

def merge():
    """ Merge two commits """

    print "You're f*cked, man. You're really f*cked"

def blame():
    """ Blame someone """

    print "So, you don't use a serious csv and you want to blame someone? Really?"

def rollback():
    """ Restore last commit """

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
        path = os.path.join(backup_dir, _f)
        if _f not in IGNORE_FILES:
            if os.path.isdir(path):
                shutil.copytree(path, '.')
            else:
                shutil.copy(path, '.')
    # restore not versione file from temp
    #last_backup = get_last_backup()
    #copy_tree(last_backup, '.')

    print "Rollback from %s" % backup_dir

def branch(branch_name):
    """ Create a new branch as a folder """

    set_current_branch(branch_name)
    path = os.path.join(BRANCHES_FOLDER, branch_name)
    if not os.path.exists(path):
        os.makedirs(path)
    print "Switched to branch %s" % branch_name

def help():
    """ Print commands list """

    print "Welcome to TiG help\n"
    print "List of available commands: \n"
    print "tig init     \t\t init a new repository"
    print "tig status   \t\t check the repository status"
    print "tig commit   \t\t commit all files and directories"
    print "tig merge    \t\t perform a merge (maybe...)"
    print "tig push     \t\t push your commits (maybe...)"
    print "tig branch   \t\t create a new branch"
    print "tig blame    \t\t blame someone!"
    print "tig rollback \t\t revert your modification"
    print "tig log      \t\t show the repo history"
    print "tig help     \t\t display this help page"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('command', nargs='?')
    parser.add_argument('param', nargs='?')
    args = parser.parse_args()

    if not args.command:
        help()
    else:
        try:
            if args.command not in AVAILABLE_COMMANDS:
                print "Command '%s' not found. Available commands are: %s." \
                % (args.command, ", ".join(cmd for cmd in AVAILABLE_COMMANDS))
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
