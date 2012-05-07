from tables import *
import tables


class TestBackend:

  def __init__(self, filename, mode):

    self.mode = mode

    if mode == "w":
      self.h5file = openFile(filename, mode, title = "test file")

      keyLen = 150
      valueLen = 400

      class Item(IsDescription):
        key = StringCol(keyLen)
        value = StringCol(valueLen)

      self.table = self.h5file.createTable('/', 'testdb', Item)
      self.test_db_items = self.table.row

    elif mode == "r":
      self.table = tables.openFile(filename)
      self.test_db_items = self.table.root.testdb
      self.next_rec_num = 0   # Initialise next record counter
      self.num_records = len(self.test_db_items)

  def __setitem__(self, key, value):

    self.test_db_items['key'] = key
    self.test_db_items['value'] = value
    self.test_db_items.append()

  def __getitem__(self, key):

    return self.test_db_items[key]

  def __len__(self):

    return len(self.test_db_items)

  def first(self):

    return (self.test_db_items[0][0], self.test_db_items[0][1])

  def iteritems(self):

    while(self.next_rec_num < self.num_records):
      key = self.test_db_items[self.next_rec_num][0]
      value = self.test_db_items[self.next_rec_num][1]
  
      self.next_rec_num += 1

      yield (key, value)

  def close(self):

    self.table.flush()

    if self.mode == "w":
      self.h5file.close()

