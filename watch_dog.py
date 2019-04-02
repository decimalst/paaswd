import sqlite3
import sys
import argparse
import os
import time
import datetime

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--passwd-file', default="/etc/passwd",
                    help='Path to passwd file, defaults to /etc/passwd')
parser.add_argument('--group-file', default="/etc/group",
                    help='Path to passwd file, defaults to /etc/group')
parser.add_argument('--database-path', default="/tmp/watch_dog_db.sqlite",
                    help='Path to database file, defaults to /tmp/watch_dog_db.sqlite')
parser.add_argument('--log-file-path', default="/tmp/watch_dog.log",
                    help='Path to database file, defaults to /tmp/watch_dog.log')
parser.add_argument('--setup-db-only', default=False, required=False, action="store_true",
                    help='Optional argument to initialize the database file')

args = parser.parse_args()

passwd_file_path = args.passwd_file
group_file_path = args.group_file
database_file_path = args.database_path
log_file_path = args.log_file_path
setup_db_only = args.setup_db_only


try:
    open(passwd_file_path, 'r')
    open(group_file_path, 'r')
    open(database_file_path, 'w')
    open(log_file_path, 'w')
except IOError as e:
    print(e)
    sys.exit(1)

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

def write_group_changes(conn):
    group_file = open("/etc/group", 'r')
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
    group_file.close()

def write_passwd_changes(conn):
    passwd_file = open("/etc/passwd", 'r')
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
    passwd_file.close()


log = open(log_file_path,'w')

conn = sqlite3.connect(database_file_path)
if setup_db_only:
    try:
        table_create(conn)
    except Exception as e:
        print(e)
        print("Error, could not create database.")
        sys.exit(1)
    finally:
        conn.close()
        sys.exit(0)

table_create(conn)
conn.commit()

while True:
    try:
        write_passwd_changes(conn)
        write_group_changes(conn)
        log.write(str(datetime.datetime.now())+ " writing new changes to db")
        time.sleep(10)
    except KeyboardInterrupt:
        conn.close()
        break


