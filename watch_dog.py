import pyinotify as pyi
import sqlite3
import sys
import functools
import argparse
import os
from time import sleep

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--passwd-file', default="/etc/passwd",
                    help='Path to passwd file, defaults to /etc/passwd')
parser.add_argument('--group-file', default="/etc/group",
                    help='Path to passwd file, defaults to /etc/group')
parser.add_argument('--database-path', default="/tmp/watch_dog_db.sqlite",
                    help='Path to database file, defaults to /tmp/watch_dog_db.sqlite')
parser.add_argument('--log-file-path', default="/tmp/watch_dog.log",
                    help='Path to database file, defaults to /tmp/watch_dog.log')

args = parser.parse_args()

passwd_file_path = args.passwd_file
group_file_path = args.group_file
database_file_path = args.database_path
log_file_path = args.log_file_path


try:
    open(passwd_file_path, 'r')
    open(group_file_path, 'r')
    open(database_file_path, 'w')
    open(log_file_path, 'w')
except IOError as e:
    print(e)
    sys.exit(1)

class GroupPasswdEvent(pyi.ProcessEvent):
    def my_init(self, log_file, db_path,passwd_path,group_path):
        """
        This is your constructor it is automatically called from
        ProcessEvent.__init__(), And extra arguments passed to __init__() would
        be delegated automatically to my_init().
        """
        self.log_file = log_file
        self.db_path = db_path
        self.passwd_path = passwd_path
        self.group_path = group_path

    def process_default(self, event):
        """
        Eventually, this method is called for all others types of events.
        This method can be useful when an action fits all events.
        """
        print(str(event))
        if event.path == passwd_file_path:
            self.write_passwd_changes()
            print("would write pwd file here")
        if event.path == group_file_path:
            self.write_group_changes()
            print("would write group file here")
        print("in close_write event")

    def write_group_changes(self):
        group_file = open("/etc/group", 'r')
        conn = sqlite3.connect(self.db_path)
        delete = "DELETE FROM USER_GROUP;"
        insert = "INSERT OR REPLACE INTO USER_GROUP (GROUP_NAME, GID, GROUP_LIST) VALUES (?,?,?)"
        rows = []
        for i in group_file:
            row = i.strip("\n").split(":")
            del(row[1])
            rows.append(row)
        conn.execute(delete)
        conn.executemany(insert,rows)
        conn.commit()
        conn.close()
        group_file.close()
        print("in group_changes")

    def write_passwd_changes(self):
        passwd_file = open("/etc/passwd", 'r')
        conn = sqlite3.connect(self.db_path)
        delete = "DELETE FROM USER_PASSWD;"
        insert = "INSERT OR REPLACE INTO USER_PASSWD (USERNAME,UID,GID,INFO, HOME_DIR,SHELL) VALUES (?,?,?,?,?,?);"
        rows = []
        for i in passwd_file:
            row = i.strip("\n").split(":")
            del(row[1])
            rows.append(row)
        conn.execute(delete)
        conn.executemany(insert,rows)
        conn.commit()
        conn.close()
        passwd_file.close()
        print("in write_passwd_changes")

    def clean_up(self):
        self.log_file.close()

def table_create(connection):
    #iterate through files in ./sql directory
    for filename in os.listdir("./sql/"):
        if filename.endswith(".sql"): 
            our_sql = open(os.path.join("./sql/", filename), 'r').read()
            sqlite3.complete_statement(our_sql)
            cursor = connection.cursor()
            try:
                cursor.executescript(our_sql)
            except Exception as e:
                print(e)
                cursor.close()
        else:
            continue

def initial_load(connection,GroupPasswdEventhandler):
    GroupPasswdEventhandler.write_group_changes(None)
    GroupPasswdEventhandler.write_passwd_changes(None)

watches = []
watches.append(passwd_file_path)
watches.append(group_file_path)
#we only really care if this file is changed, not if it's opened

log = open(log_file_path,'w')

conn = sqlite3.connect(database_file_path)
table_create(conn)
conn.commit()
conn.close()
pyi.log.setLevel(10)
try:
    wm = pyi.WatchManager()
    event_handler = GroupPasswdEvent(log_file=log,db_path=database_file_path,passwd_path=passwd_file_path,group_path=group_file_path)
    wm.add_watch(watches, pyi.IN_CLOSE_WRITE)
    notifier = pyi.Notifier(wm,event_handler,read_freq=5,threshold=64,timeout=500)
    notifier.loop()
finally:
    print("Closing files")
    event_handler.clean_up()