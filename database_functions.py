import sys, datetime, sqlite3
from pprint import pprint
from time import time, gmtime, strftime, mktime, localtime

sys.dont_write_bytecode = True

ROWS = {'1':'A',
        '2':'B',
        '3':'C',
        '4':'D',
        '5':'E',
        '6':'F',
        '7':'G',
        '8':'H',
        '9':'I',
        '10':'J',
        '11':'K',
        '12':'L'}

class sqlite_database:
  def __init__(self, db_file, rack_dimensions):
    # self.db = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    self.db = sqlite3.connect(db_file)

    self.db.execute("""
      CREATE TABLE IF NOT EXISTS tube_data (
        id          INTEGER    PRIMARY    KEY, 
        accn        TEXT, 
        rackNum     TEXT,
        rackDate    DATE, 
        col         TEXT, 
        row         TEXT,
        debug       TEXT,
        timeFiled   TIMESTAMP) 
      """)
    
    self.cursor         = self.db.execute('SELECT max(id) FROM tube_data')
    self.max_id         = self.cursor.fetchone()[0]
    self.column_width   = rack_dimensions['columns']
    self.row_height     = rack_dimensions['rows']
    self.days_stored    = 1

    self.next_row       = None
    self.next_rack      = None
    self.next_column    = None
    self.rack_date      = datetime.datetime.combine(datetime.date.today(), datetime.time())
    self.locate_next()

  def locate_next(self):
    self.cursor = self.db.execute('SELECT max(id) FROM tube_data')
    self.max_id = self.cursor.fetchone()[0]
    print self.cursor.rowcount
    if self.max_id is None:
      print "omg fucking work"
      self.max_id       = 0
      self.next_row     = 1
      self.next_column  = 1
      self.next_rack    = 1
      return;
    self.cursor = self.db.execute('SELECT rackNum, col, row FROM tube_data where id is ' + str(self.max_id))
    last_entry  = self.cursor.fetchone()
    rack        = int(last_entry[0])
    column      = int(last_entry[1])
    row         = int(last_entry[2])
    if column == self.column_width: 
      if row == self.row_height:
        column  =   1
        row     =   1
        rack    +=  1
      else:
        column  = 1
        row     += 1
    else:
      column += 1

    nextSpot = [str(rack), str(column), str(row)]
    self.next_row     = row
    self.next_rack    = rack
    self.next_column  = column
    return nextSpot
    
  def find_accn(self, accn):
    self.cursor = self.db.cursor()
    rows = []
    # this gets a datetime of midnight a few days ago. 
    earliest_date = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(self.days_stored), datetime.time())
    print earliest_date
    try:
      self.cursor.execute("""
        SELECT id, accn, rackNum, col, row, timeFiled, debug FROM tube_data WHERE accn == ? AND 
        rackDate >= DATE(?) ORDER BY id DESC""",(accn, earliest_date,))
    except sqlite3.Error as e:
      print "SQLite Error:", e.args[0]
      #this might not be needed, returning "self.cursor" might work. 
    for thing in self.cursor:
      print thing
      rows.append(thing)
    for row in rows:
      pprint(row)
    return rows

  def find_all(self):
    self.cursor = self.db.cursor()
    today = int(mktime(datetime.date.today().timetuple()))
    yesterday = int(mktime((datetime.date.today() - datetime.timedelta(1)).timetuple()))
    twoDaysAgo = int(mktime((datetime.date.today() - datetime.timedelta(2)).timetuple()))
    print "Today", today
    dates = [twoDaysAgo, yesterday, today]
    rows = []
    setRows = orderedset.OrderedSet()
    for date in dates:
      try:
        self.cursor.execute("SELECT id, accn FROM tube_data WHERE timeFiled >= datetime(" + str(date) + ", 'unixepoch', 'localtime') AND timeFiled <= datetime(" + str(date + 86399) + ", 'unixepoch', 'localtime')s ORDER BY id ASC")
      except sqlite3.Error as e:
        print "SQLite Error:", e.args[0];
      else:
        for item in self.cursor:
          print item
          setRows.add(item[1])
    for x in setRows:
      print x
    print "----"
    while setRows:
      rows.append(setRows.pop())
    return rows

  def file_accn(self, accn):
    self.locate_next()
    time_filed = time()
    print time_filed
    self.db.execute("INSERT INTO tube_data (accn, rackNum, rackDate, timeFiled, col, row) VALUES(?,?,?,?,?,?)", 
                    (accn, self.next_rack, self.rack_date, time_filed, self.next_column, self.next_row))
    self.db.commit()
    self.locate_next()

def testDB(dbclass):
  test = 0
  accn = "012546308014"
  while test < 10:
    dbclass.file_accn(accn)
    print "file loop"
    test +=1
  pprint(dbclass.find_accn(accn))

# this function is to remove an item from a tuple, not really a database function
def tuple_without(original_tuple, element_to_remove):
    new_tuple = []
    for s in list(original_tuple):
        if not s == element_to_remove:
            new_tuple.append(s)
    return tuple(new_tuple)


if __name__ == '__main__':
  rack_dimensions = {'columns': 6, 'rows': 12}
  test = sqlite_database('racks.db', rack_dimensions)
  print "file_accn function"
  test.file_accn("98765")
  print "find accn"
  test.find_accn("98765")
  # test.find_all()
  test.db.close()
