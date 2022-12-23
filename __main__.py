
# -*- coding: utf-8 -*-
import sys
import main
from gunicorn.app.wsgiapp import run
sys.argv.append('main:app')
sys.exit(run(host='0.0.0.0',workers=8))

# from main import run

# run()