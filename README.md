# About Replica Folder Synchronization

Short Python script to synchronize two folders, source and replica. 
The challenge was not to use a third-party library like rsync to implement the synchronization.

Synchronizations works only one way and can be performed periodically. File and folder creation, copying and removal are logged into a logfile.

The script to perform a **single synchronization** is `sync_folders.py`.


There is two versions of calling this synchronization **periodically**: 
- In the script `sync_task_v1.py` the synchronization is performed periodically via a while loop. 
- In the script `sync_task_v2.py` the synchronization is performed periodically via setting up a task in windows task scheduler.







## How to use

It is possible to run a **single synchronization** by calling `sync_folders.py`.
This script has 3 required inputs:

    - -s or --fld_src: Path to the source folder which is to be synchronized
    - -r or --fld_sync: Path to the replica folder
    - -l or --fld_log: Path to the folder in which the logfile will be created
	

	
	
**Synchronization periodically via a while loop**: The script `sync_task_v1.py` has 5 inputs of which 3 are required:

    - -s or --fld_src: Path to the source folder which is to be synchronized
    - -r or --fld_sync: Path to the replica folder
    - -l or --fld_log: Path to the folder in which the logfile will be created
	
	optional parameters:
	- -i or --interval: Interval of synchronizations in minutes, defaults to 1 minute
	- -d or --duration: Duration of synchronizations in minutes, defaults to 1 day
	
	


**Synchronization periodically via a task in windows task**: The script `sync_task_v2.py` has 5 inputs of which 3 are required:

    - -s or --fld_src: Path to the source folder which is to be synchronized
    - -r or --fld_sync: Path to the replica folder
    - -l or --fld_log: Path to the folder in which the logfile will be created
	
	optional parameters:
	- -i or --interval: Interval of synchronizations in minutes, defaults to 1 minute
	- -d or --duration: Duration of synchronizations in minutes, defaults to 1 day
