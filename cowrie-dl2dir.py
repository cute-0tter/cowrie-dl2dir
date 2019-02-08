#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import re
import datetime
import shutil


# -------------------- Path setting --------------------
# For downloaded files
SRC_DIR_PATH = './cowrie/var/lib/cowrie/downloads/'
#
# For TTYs
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


def is_valid_arg_num(argc, valid_arg_num):
    '''Check the number of command line arguments.

    Args:
        argc (int): Representing the number of command line arguments.
        valid_arg_num (int): Representing the correct number of command line arguments.

    Returns:
        bool: Representing the result of checking the number of
              command line arguments.
    '''
    if argc == valid_arg_num:
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
    # ----- Check command line arguments -----
    argvs = sys.argv
    argc = len(argvs)
    if not(is_valid_arg_num(argc, 2) and check_date_style(argvs[1])):
        display_usage()
        sys.exit(1)

    # ----- Set the target date and the destination directory path -----
    target_date = argvs[1]
    dst_dir_path = os.path.join(SRC_DIR_PATH, target_date, '')

    # ----- Display the signal to start processing -----
    print('[+] Start')

    # ----- Get file names in the source directory -----
    src_dir_file_names = []
    if os.path.exists(SRC_DIR_PATH):
        src_dir_file_names = get_file_names(SRC_DIR_PATH, target_date)
    else:
        print('[+] \"{0}\" was not found.'.format(SRC_DIR_PATH))
        print('[+] Done')
        sys.exit(1)

    # ----- Check the number of file names in the source directory -----
    if len(src_dir_file_names) == 0:
        print('[+] A file created on \"{0}\" was not found.'.format(target_date))
        print('[+] Done')
        sys.exit(1)

    # ----- Get file names in the destination directory -----
    dst_dir_file_names = []
    if os.path.exists(dst_dir_path):
        dst_dir_file_names = get_file_names(dst_dir_path, target_date)
    else:
        print('[+] \"{0}\" directory was not found.'.format(target_date))
        print('[+] Create \"{0}\" directory.'.format(target_date))
        os.mkdir(dst_dir_path)
        print('[+] \"{0}\" directory was created.'.format(target_date))

    # ----- Move files in the source directory to the destination directory -----
    for src_dir_file_name in src_dir_file_names:
        if src_dir_file_name in dst_dir_file_names:
            print('[+] \"{0}\" exists in \"{1}\" directory.'.format(src_dir_file_name, target_date))
        else:
            shutil.move(SRC_DIR_PATH + src_dir_file_name, dst_dir_path)
            print('[+] \"{0}\" moved to \"{1}\" directory.'.format(src_dir_file_name, target_date))

    # ----- Display the signal to finish processing -----
    print('[+] Done')


if __name__ == '__main__':
    main()
