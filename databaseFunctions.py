import sqlite3
import sys
import datetime
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
  def __init__(self, db_file):
    self.db = sqlite3.connect(db_file)
    self.db.execute("CREATE TABLE IF NOT EXISTS tube_data (id INTEGER PRIMARY KEY, accn TEXT, rackNum TEXT, timeFiled TIMESTAMP, col TEXT, row TEXT)")
    self.cursor = self.db.execute('SELECT max(id) FROM tube_data')
    self.max_id = self.cursor.fetchone()[0]

  def locateNext(self):
    self.cursor = self.db.execute('SELECT max(id) FROM tube_data')
    if self.max_id is None:
      rackNum = 1
      col = 0
      row = 1
    else:
      self.cursor = self.db.execute('SELECT rackNum, col, row FROM tube_data where id is ' + str(self.max_id))
      lastRow = self.cursor.fetchone()
      rackNum = int(lastRow[0])
      col = int(lastRow[1])
      row = int(lastRow[2])
    if col == 6 and row == 12:
      col = 1
      row = 1
      rackNum += 1
    elif col == 6 and row != 12:
      col = 1
      row += 1
    elif col != 6:
      col += 1
    nextSpot = [str(rackNum), str(col), str(row)]
    return nextSpot
    
  def findAccn(self, accn):
    self.cursor = self.db.cursor()
    today = int(mktime(datetime.date.today().timetuple()))
    yesterday = int(mktime((datetime.date.today() - datetime.timedelta(1)).timetuple()))
    twoDaysAgo = int(mktime((datetime.date.today() - datetime.timedelta(2)).timetuple()))
    print "Today", today
    dates = [today, yesterday, twoDaysAgo]
    rows = []
    for date in dates:
      try:
        self.cursor.execute("SELECT id, rackNum, col, row FROM tube_data WHERE accn == '"+accn+"' AND timeFiled >= datetime(" + str(date) + ", 'unixepoch', 'localtime') AND timeFiled <= datetime(" + str(date + 86399) + ", 'unixepoch', 'localtime') ORDER BY id DESC")
      except sqlite3.Error as e:
        print "SQLite Error:", e.args[0]
      else:
        for thing in self.cursor:
          # print thing
          rows.append(thing + (strftime("%m%d%y", localtime(date)),))
    pprint(rows)
    return rows

  def findAll(self):
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
      except sqlite3.OperationalError:
        print "SQLite DB locked"
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

  def fileAccn(self, accn):
    loc = self.locateNext()
    timeFiled = datetime.datetime.now()
    self.cursor = self.db.execute("INSERT INTO tube_data (accn, rackNum, timeFiled, col, row) VALUES(?,?,?,?,?)", (accn, loc[0], timeFiled, loc[1], loc[2]))
    self.db.commit()

  def lastFiled(self):
    # max_id = self.cursor.fetchone()[0]
    if self.max_id is None:
      return None
    else:
      self.cursor = self.db.execute('SELECT rackNum, col, row, accn FROM tube_data where id is ' + str(self.max_id))
      lastFiled = self.cursor.fetchone()
      return lastFiled

def testDB(dbclass):
  test = 0
  accn = "012546308014"
  while test < 10:
    dbclass.fileAccn(accn)
    test +=1
  pprint(dbclass.findAccn(accn))

def tuple_without(original_tuple, element_to_remove):
    new_tuple = []
    for s in list(original_tuple):
        if not s == element_to_remove:
            new_tuple.append(s)
    return tuple(new_tuple)


if __name__ == '__main__':
  test = sqlite_database('racks.db')
  test.fileAccn("123456")
  testDB(test)
  test.findAccn("123456")
  # test.findAll()
  test.db.close()



  # db = sqlite3.connect('racks.db')
  
  # db.close()
  # testDB()



