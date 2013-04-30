#!/bin/bash
AMAO_USER=$1

echo "entrando no VirtualEnv AMAO"
workon AMAO

echo "parando django"
./AMAO/stop_server.sh

echo "parando celery e celerybeat"
/etc/init.d/celeryd stop
/etc/init.d/celerybeat stop



echo "atualizando codigo fonte"
sudo -H -u ${AMAO_USER} git pull origin deploy

echo "recoletando statics"
./AMAO/manage.py collectstatic --dry-run --noinput



echo "limpando pycs"
clear_pyc

echo "reiniciando celerybeat e celery"
/etc/init.d/celerybeat start
/etc/init.d/celeryd start

echo "iniciando django"
./AMAO/run_server.sh


echo "saindo do VirtualEnv AMAO"
deactivate
