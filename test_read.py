#open file
import sqlite3
passwd_file = open('/etc/passwd', 'r')
conn = sqlite3.connect('test.db')
insert = "INSERT INTO USER_PASSWD (USERNAME,UID,GID,INFO, HOME_DIR,SHELL) VALUES (?,?,?,?,?,?);"
rows = []
for i in passwd_file:
	row = i.strip("\n").split(":")
	del(row[1])
	rows.append(row)
conn.executemany(insert,rows)
conn.commit()
out = conn.execute("SELECT * FROM USER_PASSWD")
for i in out:
	print(i)