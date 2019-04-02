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

### If using Vagrant:
1. Clone the repository.
2. Run the vagrant file with "vagrant up" - This should run the provisioning steps in the vagrant file.
3. ssh into the machine, and run the /opt/paaswd/watch_dog.py as a user with access to the /etc/paaswd and /etc/group files, that can write to /tmp/ via python3 watch_dog.py
4. Start the flask app with sh run.sh

### If installing on a bare VM:
1. Place all repo files in a directory /opt/paaswd/ on a server.
2. Run the script /opt/paaswd/watch_dog.py as a user with access to the /etc/paaswd and /etc/group files, that can write to /tmp/ via python3 watch_dog.py
3. Modify run.sh to have host=127.0.0.1 as the argument to "flask run", then run it with 'sh run.sh'


## Design justification:

Basically, I didn't want to have a webservice running at a permission level that would let it read /etc/passwd/.
The watchdog process has read-write access to the sqlite database, and elevated privileges to look at /etc/passwd, but the flask webapp would technically need read-only access. This setup at least adds a buffer where if the webapp is broken for remote code execution, an attacker also needs to find a privilege escalation exploit on the system.