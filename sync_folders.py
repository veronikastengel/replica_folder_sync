#!/usr/bin/env python
# coding: utf-8

# ------------------------------------#
# Version:        1.0.0               #
# Modified:       31.02.2023          #
# Pythonversion:  3.9.13              #
# Author:         Veronika Stengel    #
# ------------------------------------#

import os, shutil, logging
from datetime import datetime
from optparse import OptionParser

def sync_folders(fld_src, fld_sync, log_file):
    #start logging
    log_name = f"log_{datetime.now().strftime('%Y%m%d')}.log"
    logging.basicConfig(filename=os.path.join(log_file, log_name), level=logging.INFO, format='%(asctime)s - %(message)s')

    #create console logger
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logging.getLogger('').addHandler(console)
    
    #check inputs quality
    if not os.path.isdir(fld_src):
        logging.error(f"Source folder '{fld_src}' does not exist or is not a directory")
        raise ValueError(f"Source folder '{fld_src}' does not exist or is not a directory")

    if os.path.exists(fld_sync):
        if not os.path.isdir(fld_sync):
            logging.error(f"Target folder '{fld_sync}' already exists but is not a directory")
            raise ValueError(f"Target folder '{fld_sync}' already exists but is not a directory")
        if not os.access(fld_sync, os.W_OK):
            logging.error(f"Target folder '{fld_sync}' already exists but user does not have writing privileges")
            raise ValueError(f"Target folder '{fld_sync}' already exists but user does not have writing privileges")
    else:
        if not os.access(os.path.dirname(fld_sync), os.W_OK):
            logging.error(f"Target folder '{fld_sync}' can't be created, user does not have writing privileges")
            raise ValueError(f"Target folder '{fld_sync}' can't be created, user does not have writing privileges")
        os.mkdir(fld_sync)

    #DELETE - from deepest level outwards
    for root, dirs, files in os.walk(fld_sync, topdown=False):
        relative_path = os.path.relpath(root, fld_sync)
        source_dir = os.path.join(fld_src, relative_path)

        for file in files:
            source_file = os.path.join(source_dir, file)
            target_file = os.path.join(root, file)

            if not os.path.exists(source_file):
                os.remove(target_file)
                logging.info(f"Deleted file {target_file}")

        for dir in dirs:
            source_subdir = os.path.join(source_dir, dir)
            target_subdir = os.path.join(root, dir)

            if not os.path.exists(source_subdir):
                shutil.rmtree(target_subdir)
                logging.info(f"Deleted folder {target_subdir}")

                
    #INSERT / UPDATE
    for root, dirs, files in os.walk(fld_src):
        relative_path = os.path.relpath(root, fld_src)
        target_dir = os.path.join(fld_sync, relative_path)

        if not os.path.exists(target_dir):
            os.mkdir(target_dir)
            logging.info(f"Created folder {target_dir}")

        for file in files:
            source_file = os.path.join(root, file)
            target_file = os.path.join(target_dir, file)

            if not os.path.exists(target_file) or\
                    os.path.getmtime(source_file) != os.path.getmtime(target_file) or\
                    os.path.getsize(source_file) != os.path.getsize(target_file):
                shutil.copy2(source_file, target_file)
                logging.info(f"Copied file {source_file} to {target_file}")
                
    logging.info("Sync completed\n")

if __name__ == "__main__":

    ######### command line options
    parser = OptionParser()
    parser.add_option("-s", "--fld_src", dest="fld_src")
    parser.add_option("-r", "--fld_sync", dest="fld_sync")
    parser.add_option("-l", "--fld_log", dest="fld_log")
    options, _ = parser.parse_args()
    ######### command line options

    scriptPath =  os.path.dirname(__file__)
    log_file_path = os.path.join(scriptPath, options.fld_log)

    sync_folders(options.fld_src, options.fld_sync, log_file_path)