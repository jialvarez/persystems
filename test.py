# This file is part of Persistence Systems
#
# This software is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this package; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

"""
  A brief comparison into persistence systems for Python

  Currently comparing following systems:
  + bsddb
  + pytables
  + durus
  + zodb
  + redis

  This module contains the main program that executes tests reading
  and writing process, measuring time to end both read and write process
"""

__author__ = "Jose I. Alvarez <neonigma@gmail.com>"
__copyright__ = "Copyright 2011, Jose I. Alvarez <neonigma@mail.com>"
__license__ = "GPL-2"

import csv
import time
import getopt
import imp
import os

# CSV to process
FILENAME = '/tmp/fichero1.csv'


class Test:

  def __init__(self, csv_reader, module):

    # import backend
    f, filename, description = imp.find_module(module, ['backends'])
    try:
        moduleObj = imp.load_module(module, f, filename, description)
    finally:
        f.close()

    # open test write database for chosen backend
    test_file = '/tmp/test' + module + '.db'
    test_db = moduleObj.TestBackend(test_file, "w")

    # start write test to disk
    start_write = time.time()

    i = 0
    for row in csv_reader:
      test_db[str(i)] = str(row)
      i += 1

    test_db.close()

    end_write = time.time()

    print module + " writing time: " + str(end_write - start_write)

    # start read test to memory from disk
    start_read = time.time()

    test_db = moduleObj.TestBackend(test_file, "r")

    # Read records. PyTables uses a different way based on class description
    for item in test_db.getTestDBItems():
      if module == 'pytables':
        a = item['key']
        b = item['value']
      else:
        memvar = item

    #Another way to read records, unimplemented by now
    #for (key, value) in test_db.iteritems():
    #  memvar = value
    #  i += 1

    test_db.close()

    end_read = time.time()

    print module + " reading time: " + str(end_read - start_read) + "\n"


def getCSVReader():

  # CSV dialect where lines end in "\n"
  csv.register_dialect('endline', lineterminator='\n')
  csv_reader = csv.reader(open(FILENAME,'r'), delimiter=',')
  return csv_reader

# test experiment
tester = Test(getCSVReader(), "pytables")
tester = Test(getCSVReader(), "pybsddb")
tester = Test(getCSVReader(), "pyzodb")
tester = Test(getCSVReader(), "pydurus")
tester = Test(getCSVReader(), "pyredis")
