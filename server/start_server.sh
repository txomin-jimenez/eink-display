# /bin/bash

# turn on bash's job control
set -m

# Start the web server process and put it in the background
echo Starting Eink-Display server...
gunicorn -w 2 -b 0.0.0.0:8000 eink-display-server:app &

# Start the nook watcher process
echo Starting Nook Watcher service...
python nook-watcher.py

# now we bring the server process back into the foreground
# and leave it there
fg %1
