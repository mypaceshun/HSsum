# -*- coding:utf-8 -*-
# vi: set ts=2 sw=2 et ft=python :

import os,sys
import logging

logging.basicConfig(stream = sys.stderr)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from HSsum import app as application
