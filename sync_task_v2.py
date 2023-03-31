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
import win32com.client
from optparse import OptionParser

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

    start_time = datetime.now() + timedelta(seconds=5)

    scheduler = win32com.client.Dispatch('Schedule.Service')
    scheduler.Connect()

    root_folder = scheduler.GetFolder('\\')
    task_name = f"Replica_of_Folder_{os.path.basename(fld_src)}"

    for task in root_folder.GetTasks(0):
        if task.Name == task_name:
            raise ValueError(f"Task for a replica of this folder '{fld_src}' already exists, check that first before continuing")

    task_def = scheduler.NewTask(0)
    task_def.RegistrationInfo.Description = f"Python Replica Folder Task for: {fld_src}"
    task_def.Settings.Enabled = True

    # Set the task trigger to start once, and then run every n minutes
    trigger = task_def.Triggers.Create(1)
    trigger.StartBoundary = start_time.isoformat()  # start time
    trigger.Repetition.Interval = f"PT{sync_interval}M"  # repeat every n minutes
    if sync_duration is None:
        sync_duration = 1440 # 1 day in minutes, max duration
    trigger.Repetition.Duration = f"PT{sync_duration}M"  # repeat duration, in minutes

    # Set the task action to run the Python script
    sync_script = os.path.join(scriptPath, "sync_folders.py")
    action = task_def.Actions.Create(0)
    action.Path = "python.exe"
    action.Arguments = f"{sync_script} -s {fld_src} -r {fld_sync} -l {fld_log}"

    # Register the task
    root_folder.RegisterTaskDefinition(
        task_name,
        task_def,
        6,  # TASK_CREATE_OR_UPDATE
        "", "",  # no user or password set
        0  # run as the local system account
    )

if __name__ == "__main__":
    # Version 2
    # Synchronization performed periodically via setting up a task in windows task scheduler
    sync_task(options.fld_src, options.fld_sync, options.fld_log, options.sync_interval, options.sync_duration)
