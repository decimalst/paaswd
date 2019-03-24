import pyinotify as pyi
import sqlite3
import sys
import functools

def write_passwd_changes(connection):
    passwd_file = open('/etc/passwd', 'r')
    insert = "INSERT INTO USER_PASSWD (USERNAME,UID,GID,INFO, HOME_DIR,SHELL) VALUES (?,?,?,?,?,?);"
    rows = []
    for i in passwd_file:
        row = i.strip("\n").split(":")
        del(row[1])
        rows.append(row)
    connection.executemany(insert,rows)
    connection.commit()
    out = connection.execute("SELECT * FROM USER_PASSWD")

#example mostly taken from here: https://github.com/seb-m/pyinotify/blob/master/python2/examples/loop.py

wm = pyi.WatchManager()

#we only really care if this file is changed, not if it's opened
wm.add_watch('/home/vagrant/my_file', pyi.IN_MODIFY)

#Notifier should kick off a process to update sqlite database
notifier = pyi.Notifier(wm)



conn = sqlite3.connect('test.db')

print "Opened database successfully";

write_func = functools.partial(write_passwd_changes, conn)

# Notifier instance spawns a new process when daemonize is set to True. This
# child process' PID is written to /tmp/pyinotify.pid (it also automatically
# deletes it when it exits normally). Note that this tmp location is just for
# the sake of the example to avoid requiring administrative rights in order
# to run this example. But by default if no explicit pid_file parameter is
# provided it will default to its more traditional location under /var/run/.
# Note that in both cases the caller must ensure the pid file doesn't exist
# before this method is called otherwise it will raise an exception.
# /tmp/pyinotify.log is used as log file to dump received events. Likewise
# in your real code choose a more appropriate location for instance under
# /var/log (this file may contain sensitive data). Finally, callback is the
# above function and will be called after each event loop.
try:
    notifier.loop(daemonize=True, callback=write_func,
                  pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
except pyi.NotifierError, err:
    print >> sys.stderr, err

notifier.loop()