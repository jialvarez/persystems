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
  Backend for Redis persistence system  

  This module contains minimal operations to measure time of execution
  for Redis persistence system
"""

__author__ = "Jose I. Alvarez <neonigma@gmail.com>"
__copyright__ = "Copyright 2011, Jose I. Alvarez <neonigma@mail.com>"
__license__ = "GPL-2"


import redis

class TestBackend:

  def __init__(self, filename, mode):

    self.mode = mode

    if mode == "w":
      self.test_db_items = redis.Redis()

    elif mode == "r":
      self.test_db_items = redis.Redis()

      self.next_rec_num = 0   # Initialise next record counter
      self.num_records = len(self.test_db_items.keys())

  def __setitem__(self, key, value):

    self.test_db_items.set(key, value)

  def __getitem__(self, key):

    return self.test_db_items.get(str(key))

  def __len__(self):

    return len(self.test_db_items.keys())

  def first(self):

    return self.test_db_items.get(self.test_db_items.keys()[0])

  def iteritems(self):

    while(self.next_rec_num < self.num_records):
      key = self.test_db_items.keys()[self.next_rec_num]
      value = self.test_db_items.get(key)
  
      self.next_rec_num += 1

      yield value

  def close(self):

    pass

  def getTestDBItems(self):

    return [self.test_db_items.get(key) for key in self.test_db_items.keys()]
