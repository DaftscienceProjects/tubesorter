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

def lastFiled():
  db = sqlite3.connect('racks.db')
  cursor = db.execute('SELECT max(id) FROM tube_data')
  max_id = cursor.fetchone()[0]
  if max_id is None:
    return None
  else:
    cursor = db.execute('SELECT rackNum, col, row, accn FROM tube_data where id is ' + str(max_id))
    lastFiled = cursor.fetchone()
    return lastFiled

def locateNext():
  db = sqlite3.connect('racks.db')
  cursor = db.execute('SELECT max(id) FROM tube_data')
  max_id = cursor.fetchone()[0]
  if max_id is None:
    rackNum = 1
    col = 0
    row = 1
  else:
    cursor = db.execute('SELECT rackNum, col, row FROM tube_data where id is ' + str(max_id))
    lastRow = cursor.fetchone()
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
  db.close()
  return nextSpot
  
def tuple_without(original_tuple, element_to_remove):
    new_tuple = []
    for s in list(original_tuple):
        if not s == element_to_remove:
            new_tuple.append(s)
    return tuple(new_tuple)
  
def findAccn(accn):
  db = sqlite3.connect('racks.db')
  cursor = db.cursor()
  today = int(mktime(datetime.date.today().timetuple()))
  yesterday = int(mktime((datetime.date.today() - datetime.timedelta(1)).timetuple()))
  twoDaysAgo = int(mktime((datetime.date.today() - datetime.timedelta(2)).timetuple()))

  print "Today", today

  dates = [today, yesterday, twoDaysAgo]
  rows = []
  for date in dates:
    try:
      cursor.execute("SELECT id, rackNum, col, row FROM tube_data WHERE accn == '"+accn+"' AND timeFiled >= datetime(" + str(date) + ", 'unixepoch', 'localtime') AND timeFiled <= datetime(" + str(date + 86399) + ", 'unixepoch', 'localtime') ORDER BY id DESC")
    except sqlite3.Error as e:
      print "SQLite Error:", e.args[0]
    else:
      for thing in cursor:
        # print thing
        rows.append(thing + (strftime("%m%d%y", localtime(date)),))
#  db.close()
  return rows


def findAll():
#  print accn
  db = sqlite3.connect('racks.db')
  cursor = db.cursor()
  today = int(mktime(datetime.date.today().timetuple()))
  yesterday = int(mktime((datetime.date.today() - datetime.timedelta(1)).timetuple()))
  twoDaysAgo = int(mktime((datetime.date.today() - datetime.timedelta(2)).timetuple()))
  print "Today", today

  dates = [twoDaysAgo, yesterday, today]
  rows = []
  setRows = orderedset.OrderedSet()
  for date in dates:
    #Getting the Day string
    try:
      cursor.execute("SELECT id, accn FROM tube_data WHERE timeFiled >= datetime(" + str(date) + ", 'unixepoch', 'localtime') AND timeFiled <= datetime(" + str(date + 86399) + ", 'unixepoch', 'localtime')s ORDER BY id ASC")
    except sqlite3.OperationalError:
      print "SQLite DB locked"
    else:
      # setRows = orderedset.OrderedSet()
      for item in cursor:
        print item
        setRows.add(item[1])
#  db.close()
  # setRows = set(rows)
  for x in setRows:
    print x
  print "----"
  while setRows:
    rows.append(setRows.pop())
  # rows.reverse()
  return rows

# findAll()


def fileAccn(accn):
  loc = locateNext()
  db = sqlite3.connect('racks.db')
  timeFiled = datetime.datetime.now()
  cursor = db.execute("INSERT INTO tube_data (accn, rackNum, timeFiled, col, row) VALUES(?,?,?,?,?)", (accn, loc[0], timeFiled, loc[1], loc[2]))
  db.commit()
  db.close()

def testDB():
  test = 0
  accn = "012546308014"
  while test < 10:
    fileAccn(accn)
    test +=1
  pprint(findAccn(accn))

if __name__ == '__main__':
  db = sqlite3.connect('racks.db')
  db.execute("CREATE TABLE IF NOT EXISTS tube_data (id INTEGER PRIMARY KEY, accn TEXT, rackNum TEXT, timeFiled TIMESTAMP, col TEXT, row TEXT)")
  db.close()
  testDB()



