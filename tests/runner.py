import os
import sys
path = os.path.abspath(__file__ + '/../..')
sys.path.insert(0, path)

import doctest

import pyrelite.simpledb
doctest.testmod(pyrelite.simpledb)

import pyrelite.fql
doctest.testmod(pyrelite.fql)
