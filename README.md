# paaswd

## Requirements
- Virtualbox (if running from Mac/windows)
- Vagrant (Or some other way to bring up a basic linux server images)
- Python
- pip
- Flask

## How this works:

Paaswd gives read-only access to a linux system's /etc/passwd file.

It consists of two scripts, one which watches the /etc/passwd file for changes and writes changes to a sqlite database, and a Flask-based webapp which allows queries to the underlying database.

## Setup

1. Clone the repository.
2. Run the vagrant file with "vagrant up"
1. Run watch_dog.py as a user with access to read /etc/passwd and /etc/groups and write to /tmp/, or
2. Run watch_dog.py with the command line arguments --group-file and --passwd-file with paths to copies of /etc/passwd which our user has read access to.
3. Run our flask web-app. 


## Design justification:

Basically, I didn't want to have a webservice running at a permission level that would let it read /etc/passwd/.
The watchdog process has read-write access to the sqlite database, and elevated privileges to look at /etc/passwd, but the flask webapp would technically need read-only access. This setup at least adds a buffer where if the webapp is broken for remote code execution, an attacker also needs to find a privilege escalation exploit on the system.