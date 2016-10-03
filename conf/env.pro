[global]
program=MYBI-CI
log_dir=/tmp
log_file=mybi-ci.log
log_level=
log_format=
# False, each task logs to its file and its ancestors file
# True, every task logs to the global file, not able to get the log through the server /log api call
# If True, everything is in one file and could be messy. Each build has a uuid in the log where you can grep.
log_consolidate_only=False
#server port
server_port=5000