# Example: daemonize pyinotify's notifier.
#
# Requires Python >= 2.5
import pyinotify
import sqlite3
import sys
import functools

def on_loop(notifier):
    """
    Dummy function called after each event loop, this method only
    ensures the child process eventually exits (after 5 iterations).
    """
    sys.stdout.write("Loop ran")
    conn = sqlite3.connect('/tmp/test.db')
    #passwd_file = open('/etc/passwd', 'r')

wm = pyinotify.WatchManager()
notifier = pyinotify.Notifier(wm)
wm.add_watch('/home/vagrant/my_file', pyinotify.ALL_EVENTS)
on_loop_func = functools.partial(on_loop)

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
    notifier.loop(daemonize=True, callback=on_loop_func,
                  pid_file='/tmp/pyinotify.pid', stdout='/tmp/pyinotify.log')
except pyinotify.NotifierError, err:
    print >> sys.stderr, err