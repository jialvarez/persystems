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
