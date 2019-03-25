import pyinotify as pyi
import sqlite3
import sys
import functools
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--passwd-file', default="/etc/passwd",
                    help='Path to passwd file, defaults to /etc/passwd')
parser.add_argument('--group-file', default="/etc/group",
                    help='Path to passwd file, defaults to /etc/group')
parser.add_argument('--database-path', default="/tmp/watch_dog_db",
                    help='Path to database file, defaults to /tmp/watch_dog_db')

args = parser.parse_args()

passwd_file_path = args.passwd_file
group_file_path = args.group_file
database_file_path = args.database_path

try:
    open(passwd_file_path, 'r')
    open(group_file_path, 'r')
    open(database_file_path, 'rw')
except IOError as e:
    print(e)
    sys.exit(1)


def write_passwd_changes(connection):
    passwd_file = open(passwd_file_path, 'r')
    insert = "INSERT INTO USER_PASSWD (USERNAME,UID,GID,INFO, HOME_DIR,SHELL) VALUES (?,?,?,?,?,?);"
    rows = []
    for i in passwd_file:
        row = i.strip("\n").split(":")
        del(row[1])
        rows.append(row)
    connection.executemany(insert,rows)
    connection.commit()
    #out = connection.execute("SELECT * FROM USER_PASSWD")

#example mostly taken from here: https://github.com/seb-m/pyinotify/blob/master/python2/examples/loop.py

wm = pyi.WatchManager()

#we only really care if this file is changed, not if it's opened
wm.add_watch('/home/vagrant/my_file', pyi.IN_MODIFY)

#Notifier should kick off a process to update sqlite database
notifier = pyi.Notifier(wm)



conn = sqlite3.connect('test.db')
##print "Opened database successfully";

write_func = functools.partial(write_passwd_changes, conn)

try:
    notifier.loop(daemonize=True, callback=write_func,
                  pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
except pyi.NotifierError, err:
    print >> sys.stderr, err

notifier.loop()