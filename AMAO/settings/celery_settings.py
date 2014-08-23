#coding: utf-8

import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "admin"
BROKER_PASSWORD = "mypass"
BROKER_VHOST = "/"
