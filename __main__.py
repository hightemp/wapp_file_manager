# -*- coding: utf-8 -*-
import sys
import main

from request_vars import *
from database import *
from baselib import *

from gunicorn.app.base import Application, Config
import gunicorn
from gunicorn import glogging
from gunicorn.workers import sync

from gunicorn.app.wsgiapp import run
sys.argv.append('main:app')
sys.exit(run())

# from main import run

# run()