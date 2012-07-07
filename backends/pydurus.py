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
  Backend for durus persistence system  

  This module contains minimal operations to measure time of execution
  for durus persistence system
"""

__author__ = "Jose I. Alvarez <neonigma@gmail.com>"
__copyright__ = "Copyright 2011, Jose I. Alvarez <neonigma@mail.com>"
__license__ = "GPL-2"


from durus.connection import Connection
from durus.file_storage import FileStorage
from durus.persistent import Persistent
from durus.persistent_dict import PersistentDict


class TestBackend:

  def __init__(self, filename, mode):

    self.mode = mode

    if mode == "w":
      self.storage = FileStorage(filename)
      self.connection = Connection(self.storage)
      self.test_db_items = self.connection.get_root()

    elif mode == "r":
      self.storage = FileStorage(filename)
      self.connection = Connection(self.storage)
      self.test_db_items = self.connection.get_root()

      self.next_rec_num = 0   # Initialise next record counter
      self.num_records = len(self.test_db_items)

  def __setitem__(self, key, value):

    self.test_db_items[key] = value

  def __getitem__(self, key):

    return self.test_db_items[str(key)]

  def __len__(self):

    return len(self.test_db_items)

  def first(self):

    return self.test_db_items[0]

  def iteritems(self):

    while(self.next_rec_num < self.num_records):
      value = self.test_db_items[self.next_rec_num]
  
      self.next_rec_num += 1

      yield value

  def close(self):
    self.connection.commit()
    self.storage.close()

  def getTestDBItems(self):
    return self.test_db_items.values()
