INSERT OR REPLACE INTO USER_PASSWD (USERNAME,UID,GID,INFO, HOME_DIR,SHELL)
 VALUES
  ('root',0,0,'','/','/bin/bash'),
  ('ubuntu',1001,1001,'','/','/bin/bash');

INSERT INTO USER_GROUP (GROUP_NAME, GID, GROUP_LIST)
VALUES
  ('root', 0, 'root'),
  ('sudo', 1001, 'ubuntu');