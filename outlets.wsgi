#!/usr/bin/python3
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/online_store/outlets")

from outlet import app as application
application.secret_key = '0vn6i8gjh81agc8bc528hpbdmn95movh'
