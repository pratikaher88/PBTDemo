#!/bin/bash

function msg(){
  echo -e "${yellow}    => ${@}${default}"
}

function msg2(){
  echo -e "${red}${@}!${default}"
}

VIRTUALENV=${VIRTUALENV:-./virtualenv}/bin/activate

if [ ! -e "${VIRTUALENV}" ]; then
  msg2 "${VIRTUALENV} does not exist"
  exit 1
fi

msg "Activating virtualenv ${VIRTUALENV} …"
source ${VIRTUALENV}

echo "Killing existing uwsgi daemon if any."
kill -9 `cat uwsgi.pid`
sleep 5
echo "Starting uwsgi daemon ..."
uwsgi --ini /home/tingtun/pbt-demo/apache_files/uwsgi.cfg --pidfile uwsgi.pid --uid tingtun --gid tingtun --chdir /home/tingtun/pbt-demo --wsgi-file pbtdemo/wsgi.py --check-static /home/tingun/pbt-demo/ # --daemonize2 yes --enable-threads

