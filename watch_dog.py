import pyinotify as pyi
import sqlite3
import sys
import functools
import argparse
import os

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--passwd-file', default="/etc/passwd",
                    help='Path to passwd file, defaults to /etc/passwd')
parser.add_argument('--group-file', default="/etc/group",
                    help='Path to passwd file, defaults to /etc/group')
parser.add_argument('--database-path', default="/tmp/watch_dog_db.sqlite",
                    help='Path to database file, defaults to /tmp/watch_dog_db.sqlite')
parser.add_argument('--log-file-path', default="/tmp/watch_dog_log",
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
    def my_init(self, log_file, connection,passwd_path,group_path):
        """
        This is your constructor it is automatically called from
        ProcessEvent.__init__(), And extra arguments passed to __init__() would
        be delegated automatically to my_init().
        """
        self.log_file = log_file
        self.sqlite_connection = connection
        self.passwd_path = passwd_path
        self.group_path = group_path

    def process_default(self, event):
        """
        Eventually, this method is called for all others types of events.
        This method can be useful when an action fits all events.
        """
        self.log_file.write(str(event) + '\n')
        self.log_file.write(str(event.path) + '\n')
        self.log_file.flush()
        if event.path == passwd_file_path:
            self.write_passwd_changes()
        if event.path == group_file_path:
            self.write_group_changes()

    def write_group_changes(self):
        group_file = open(group_file_path, 'r')
        delete = "DELETE FROM USER_GROUP;"
        insert = "INSERT OR REPLACE INTO USER_GROUP (GROUP_NAME, GID, GROUP_LIST) VALUES (?,?,?)"
        rows = []
        for i in group_file:
            row = i.strip("\n").split(":")
            del(row[1])
            rows.append(row)
        self.sqlite_connection.execute(delete)
        self.sqlite_connection.executemany(insert,rows)
        self.sqlite_connection.commit()

    def write_passwd_changes(self):
        passwd_file = open(passwd_file_path, 'r')
        delete = "DELETE FROM USER_PASSWD;"
        insert = "INSERT OR REPLACE INTO USER_PASSWD (USERNAME,UID,GID,INFO, HOME_DIR,SHELL) VALUES (?,?,?,?,?,?);"
        rows = []
        for i in passwd_file:
            row = i.strip("\n").split(":")
            del(row[1])
            rows.append(row)
        self.sqlite_connection.execute(delete)
        self.sqlite_connection.executemany(insert,rows)
        self.sqlite_connection.commit()

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
                cursor.close()
        else:
            continue
    #run each as a query

def initial_load(connection,groupPasswdEvent):
    groupPasswdEvent.write_group_changes()
    groupPasswdEvent.write_passwd_changes()

watches = []
watches.append(passwd_file_path)
watches.append(group_file_path)
#we only really care if this file is changed, not if it's opened

log = open('/tmp/watch_dog.log','w')

conn = sqlite3.connect(database_file_path)
table_create(conn)
conn.commit()

try:
    wm = pyi.WatchManager()
    # It is important to pass named extra arguments like 'fileobj'.
    event_handler = GroupPasswdEvent(log_file=log,connection=conn,passwd_path=passwd_file_path,group_path=group_file_path)
    initial_load(conn,event_handler)
    notifier = pyi.Notifier(wm, default_proc_fun=event_handler)
    wm.add_watch(watches, pyi.IN_MODIFY)
    notifier.loop()
finally:
    conn.close()
    log.close()