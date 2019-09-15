#!/usr/bin/env python3

import os
import bjoern
from pony.orm.dbproviders import sqlite
#from pony.orm.dbproviders import postgres
from fsm_web.app import application

port = int(os.environ.get("PORT", 8000))
bjoern.run(application, "", port)
# pyinstaller -y app.py
