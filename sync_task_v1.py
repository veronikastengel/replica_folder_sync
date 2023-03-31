#!/usr/bin/env python
# coding: utf-8

# ------------------------------------#
# Version:        1.0.0               #
# Modified:       31.02.2023          #
# Pythonversion:  3.9.13              #
# Author:         Veronika Stengel    #
# ------------------------------------#

import os
from datetime import datetime, timedelta
import time, schedule
from optparse import OptionParser
from sync_folders import sync_folders

######### command line options
parser = OptionParser()
parser.add_option("-s", "--fld_src", dest="fld_src")
parser.add_option("-r", "--fld_sync", dest="fld_sync")
parser.add_option("-l", "--fld_log", dest="fld_log")
parser.add_option("-i", "--interval", type="int", dest="sync_interval", default=1)
parser.add_option("-d", "--duration", type="int", dest="sync_duration", default=None)
options, _ = parser.parse_args()
######### command line options

scriptPath  = os.path.dirname(__file__)

def sync_task(fld_src, fld_sync, fld_log, sync_interval, sync_duration):

    # schedule the task to run every n minutes
    start_time = datetime.now()
    if sync_duration is None:
        sync_duration = 1440 # 1 day in minutes, max duration
    end_time = start_time + timedelta(minutes=sync_duration) + timedelta(seconds=1)


    scriptPath = os.path.dirname(__file__)
    log_file_path = os.path.join(scriptPath, fld_log)
    schedule.every(sync_interval).minutes.do(sync_folders, fld_src=fld_src, fld_sync=fld_sync, log_file=log_file_path)

    while datetime.now() < end_time:
        schedule.run_pending()
        time.sleep(sync_interval*60)

if __name__ == "__main__":
    # Version 1
    # Synchronization performed periodically via a while loop
    sync_task(options.fld_src, options.fld_sync, options.fld_log, options.sync_interval, options.sync_duration)
