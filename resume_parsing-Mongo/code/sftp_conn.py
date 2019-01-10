import pysftp
import os
import config

host = config.sftp_host
port = config.sftp_port
username = config.sftp_username
password = config.sftp_password
local_path = config.data_new
remote_path = config.remote_path

cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

# os.chdir(config.data_new)

srv = pysftp.Connection(host=host, username=username, password=password, cnopts=cnopts)
print("Connected to Server.")

for file in srv.listdir(remote_path):
    srv.get(remote_path + file, local_path + file, preserve_mtime=True)

srv.close()
print("Connection Closed.")

# TODO:
# Add check if file exist in Database. If yes then skip.
