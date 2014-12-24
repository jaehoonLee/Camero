case "$1" in 
    start)
	echo "=========================================Starting Camero Server============================================"
	nohup python manage.py runserver 0.0.0.0:9000 &
	LASTPID=$!
	echo $LASTPID > translate.pid
    ;;
    stop)
	echo "=========================================Stoping Camero Server============================================"
	CAMEROPID=$(cat /root/Camero/translate.pid)
	echo $CAMEROPID
	pkill -9 -P $CAMEROPID
    ;;
esac
exit 0
