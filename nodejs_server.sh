#!/bin/bash
#
# jboss        Startup script for the JBoss Java Application Server
#
# chkconfig: - 85 15
# description: The JBoss Java Application Server  \
#
# processname: jboss
#
SHMCCPS_HOME=/root/huykai/node_webserver/nodejs_shmcc_website
NODE=/root/huykai/node-v6.10.2-linux-x64/bin/node
start(){
        echo "Starting SHMCC PS Server.."
        $NODE $SHMCCPS_HOME/src/server_rtm.js > /tmp/nodejs_server.log 2>&1 &
        echo "Started SHMCC PS Server.."
}

stop(){
        echo "Stopping SHMCC PS Server.."
        kill -9 `ps -ef | grep server_rtm.js | grep node | awk -F' ' '{print $2}'`
        echo "Stoped SHMCC PS Server.."
}

restart(){
        stop
        # give stuff some time to stop before we restart
        sleep 2
        start
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  restart)
        restart
        ;;
  *)
        echo "Usage: service nodejs_server {start|stop|restart}"
        exit 1
esac

exit 0
