import pyinotify as pyi

#example mostly taken from here: https://github.com/seb-m/pyinotify/blob/master/python2/examples/loop.py

wm = pyi.WatchManager()

#Notifier should kick off a process to update sqlite database
notifier = pyi.Notifier(wm)

#we only really care if this file is changed, not if it's opened
wm.add_watch('/home/vagrant/my_file', pyinotify.IN_MODIFY)

notifier.loop()