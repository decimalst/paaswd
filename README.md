# paaswd

## Requirements
- Linux system with inotify kernel subsystem(so kernel > 2.6.3, aka most modern systems)
- Python
- Pyinotify(https://github.com/seb-m/pyinotify)
- Flask

## How this works:

Paaswd gives read-only access to a linux system's /etc/passwd file.

It consists of two scripts, one which watches the /etc/passwd file for changes and writes changes to a sqlite database, and a Flask-based webapp which allows queries to the underlying database.

## Setup

1. Create two users, one with permissions to access /etc/passwd and /etc/groups
2. Run watch_dog.py as the user with access to read /etc/passwd and /etc/groups
3. Run our flask webapp as the user with more minimal permissions


## Design justification:

Basically, I didn't want to have a webservice running at a permission level that would let it read /etc/passwd/.
The watchdog process has read-write access to the sqlite database, and elevated privileges to look at /etc/passwd, but the flask webapp has read-only access. This setup at least adds a buffer where if the webapp is broken for remote code execution, an attacker also needs to find a privilege escalation exploit on the system.