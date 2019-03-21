# paaswd

## Requirements
- Linux system with inotify kernel subsystem(so kernel > 2.6.3, aka most modern systems)
- Python
- Pyinotify(https://github.com/seb-m/pyinotify)
- Flask

## How this works:

Paaswd gives read-only access to a linux system's /etc/passwd file.

It consists of two scripts, one which watches the /etc/passwd file for changes and writes changes to a sqlite database, and a Flask-based webapp which allows queries to the underlying database.


## Design justification:

Basically, I didn't want to have a webservice running at a permission level that would let it read /etc/passwd/.
The watchdog process has read-write access to the sqlite database, and elevated privileges to look at /etc/passwd, but the flask webapp has read-only access. I know enough about security to know that I won't think of everything, and I figured that this setup at least adds a buffer where if the webapp is broken for remote code execution, it's not executing as root.