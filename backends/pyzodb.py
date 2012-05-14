from ZODB.FileStorage import FileStorage
from ZODB.DB import DB
import transaction


class TestBackend:

  def __init__(self, filename, mode):

    self.mode = mode

    if mode == "w":
      self.storage = FileStorage(filename)
      db = DB(self.storage)
      connection = db.open()
      self.test_db_items = connection.root()

    elif mode == "r":
      self.storage = FileStorage(filename)
      db = DB(self.storage)
      connection = db.open()
      self.test_db_items = connection.root()

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
    transaction.commit()
    self.storage.close()

  def getTestDBItems(self):
    return self.test_db_items.values()
