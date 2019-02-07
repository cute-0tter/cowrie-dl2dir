#!/bin/usr/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
import shutil
import colorama
from colorama import Fore


# -------------------- Path setting --------------------
SRC_DIR_PATH = './cowrie/var/lib/cowrie/downloads/'
# SRC_DIR_PATH = './cowrie/var/lib/cowrie/tty/'
# ------------------------------------------------------


def display_usage():
    '''Display the usage.

    Args:

    Returns:
    '''
    print('[+] Usage:')
    print('        python dl2dir.py [date]')
    print('    ex. python dl2dir.py 2019-04-01')


def check_arg_num(argc):
    '''Check the number of command line arguments.

    Args:
        argc (int): Representing the number of command line arguments.

    Returns:
        bool: Representing the result of checking the number of
              command line arguments.
    '''
    if argc == 2:
        return True
    else:
        return False


def check_date_style(target_date):
    '''Check whether the value of the command line arguments is
       appropriate date style or not.

    Args:
        target_date (list): Representing the target date.

    Returns:
        bool: Representing the result of checking wheter the value of
              the command line arguments is the appropriate date style or not.
    '''
    regex = r'^\d{4}-\d{2}-\d{2}$'
    if re.match(regex, target_date):
        return True
    else:
        return False


def get_file_names(dir_path, target_date):
    '''Get file names in a directory.

    Args:
        dir_path (str): Representing a directory path.
        target_date (str): Representing a target date.

    Returns:
        list: Representing a list containing file names in a directory.
    '''
    file_names = []
    for file_name in os.listdir(dir_path):
        target_file_path = os.path.join(dir_path, file_name)
        file_datetime_epoch = os.path.getctime(target_file_path)
        file_date = str(datetime.date.fromtimestamp(file_datetime_epoch))
        if os.path.isfile(target_file_path) and file_date == target_date:
            file_names.append(file_name)

    return file_names


def main():
    # ----- Initialize the colorama -----
    colorama.init(autoreset=True)

    # ----- Check command line arguments -----
    argvs = sys.argv
    argc = len(argvs)
    target_date = argvs[1]
    if not(check_arg_num(argc) and check_date_style(target_date)):
        display_usage()
        sys.exit(1)

    # ----- Set the destination directory path -----
    dst_dir_path = os.path.join(SRC_DIR_PATH, target_date, '')

    # ----- Display the signal to start processing -----
    print('[{0}+{1}] Start'.format(Fore.BLUE, Fore.RESET))

    # ----- Get file names in the source directory -----
    src_dir_file_names = []
    if os.path.exists(SRC_DIR_PATH):
        src_dir_file_names = get_file_names(SRC_DIR_PATH, target_date)
    else:
        print('[{0}+{1}] \"{2}\" was not found.'.format(Fore.RED, Fore.RESET, SRC_DIR_PATH))
        print('[{0}+{1}] Done'.format(Fore.BLUE, Fore.RESET))
        sys.exit(1)

    # ----- Check the number of file names in the source directory -----
    if len(src_dir_file_names) == 0:
        print('[{0}+{1}] A file created on \"{2}\" was not found.'.format(Fore.RED, Fore.RESET, target_date))
        print('[{0}+{1}] Done'.format(Fore.BLUE, Fore.RESET))
        sys.exit(1)

    # ----- Get file names in the destination directory -----
    dst_dir_file_names = []
    if os.path.exists(dst_dir_path):
        dst_dir_file_names = get_file_names(dst_dir_path, target_date)
    else:
        print('[{0}+{1}] \"{2}\" directory was not found.'.format(Fore.RED, Fore.RESET, target_date))
        print('[{0}+{1}] Create \"{2}\" directory.'.format(Fore.YELLOW, Fore.RESET, target_date))
        os.mkdir(dst_dir_path)
        print('[{0}+{1}] \"{2}\" directory was created.'.format(Fore.YELLOW, Fore.RESET, target_date))

    # ----- Move files in the source directory to the destination directory -----
    for src_dir_file_name in src_dir_file_names:
        if src_dir_file_name in dst_dir_file_names:
            print('[{0}+{1}] \"{2}\" exists in \"{3}\" directory.'.format(Fore.RED, Fore.RESET, src_dir_file_name, target_date))
        else:
            shutil.move(SRC_DIR_PATH + src_dir_file_name, dst_dir_path)
            print('[{0}+{1}] \"{2}\" moved to \"{3}\" directory.'.format(Fore.GREEN, Fore.RESET, src_dir_file_name, target_date))

    # ----- Display the signal to finish processing -----
    print('[{0}+{1}] Done'.format(Fore.BLUE, Fore.RESET))


if __name__ == '__main__':
    main()
