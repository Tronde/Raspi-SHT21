#! /bin/sh
### BEGIN INIT INFO
# Provides:          raspi-sht21
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: raspi-sht21 initscript
# Description:       This script starts the data collection with
#                    the sht21.sh script.
### END INIT INFO

# Author: Joerg Kastning <joerg.kastning@my-it-brain.de>
#
# Please remove the "Author" lines above and replace them
# with your own name if you copy and modify this script.

# Do NOT "set -e"

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Data collection with the Raspi-SHT21"
NAME=raspi-sht21.sh
DAEMON=/usr/sbin/$NAME
DAEMON_ARGS="--options args"
PIDFILE=/var/run/$NAME.pid
SCRIPTNAME=/etc/init.d/$NAME

echo $$ > $PIDFILE
case "$1" in
  start)
	echo "Starting raspi-sht21 daemon..."
	cd /home/pi/Raspi-SHT21/
	if  ./start-sht21-service.sh; then
		echo "Starting raspi-sht21 Daemon [OK]"
	else
		echo "ERROR: raspi-sht21 daemon not started." >&2
		exit 1
	fi
	;;
  stop)
	echo "Stopping raspi-sht21..." 
	killall sht21.sh
	rm -f $PIDFILE
	echo "Daemon raspi-sht21 stopped."
	;;
  status)
	#status="$(pidof /bin/sh ./sht21.sh > /dev/null; echo $?)"
	status="$(ps -fp $(cat $PIDFILE) > /dev/null; echo $?)"
	case "$status" in
		0)	echo "Deamon raspi-sht21.sh is started." ;;
		1)	echo "Deamon raspi-sht21.sh is stopped." ;;
	esac
	;;
  restart)
	echo "Stopping raspi-sht21..." 
	killall sht21.sh
	echo "Daemon raspi-sht21 stopped."
	echo "Starting raspi-sht21 daemon..."
	cd /home/pi/Raspi-SHT21/Raspi-SHT21-V3_0_0/
	if  ./start-sht21-service.sh; then
		echo "Starting raspi-sht21 Daemon [OK]"
	else
		echo "ERROR: raspi-sht21 daemon not started." >&2
		exit 1
	fi
	;;
  #reload|force-reload)
	#
	# If do_reload() is not implemented then leave this commented out
	# and leave 'force-reload' as an alias for 'restart'.
	#
	#log_daemon_msg "Reloading $DESC" "$NAME"
	#do_reload
	#log_end_msg $?
	#;;
  *)
	#echo "Usage: $SCRIPTNAME {start|stop|restart|reload|force-reload}" >&2
	echo "Usage: $SCRIPTNAME {start|stop|status|restart}" >&2
	exit 3
	;;
esac

:
