import sqlite3
import sys
import datetime
from pprint import pprint
from time import gmtime, strftime
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


def getTables():
  conn = sqlite3.connect("racks.db")
  tables = conn.cursor()
  tables.execute('select name from sqlite_master where type=\'table\'')
  rows = []
  for row in tables:
    rows.append(row)
  conn.close()
  return rows
getTables()


def newDay():
  tables = getTables()
  needNewDay = True
  today = datetime.datetime.now().strftime("%a%m%d%Y")
  for table in tables:
    if table == today:
      needNewDay = False
  if not needNewDay:
    return today  
  db = sqlite3.connect('racks.db')
  cursor = db.cursor()
  day = datetime.datetime.now().strftime("%A")
  cursor.execute("""CREATE TABLE IF NOT EXISTS """ + today + """(id INTEGER PRIMARY KEY, accn TEXT, rackNum TEXT, date TEXT, timeFiled TEXT, col TEXT, row TEXT)""")
  db.close()
  return today
newDay()


def lastFiled():
  today = str(newDay())
  db = sqlite3.connect('racks.db')
  cursor = db.execute('SELECT max(id) FROM ' + today)
  max_id = cursor.fetchone()[0]
  if max_id is None:
    return None
  else:
    cursor = db.execute('SELECT rackNum, col, row, accn FROM ' + today + ' where id is ' + str(max_id))
    lastFiled = cursor.fetchone()
    return lastFiled

def locateNext():
  today = str(newDay())
  db = sqlite3.connect('racks.db')
  cursor = db.execute('SELECT max(id) FROM ' + today)
  max_id = cursor.fetchone()[0]
  if max_id is None:
    rackNum = 1
    col = 0
    row = 1
  else:
    cursor = db.execute('SELECT rackNum, col, row FROM ' + today + ' where id is ' + str(max_id))
    lastRow = cursor.fetchone()
    rackNum = int(lastRow[0])
    col = int(lastRow[1])
    row = int(lastRow[2])
  if col == 6:
    if row == 12:
      col = 1
      row = 1
      rackNum += 1
    else:
      col = 1
      row += 1
  else:
    col += 1
  nextSpot = [str(rackNum), str(col), str(row), today[:3]]
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
  today = newDay()
  yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime("%a%m%d%Y")
  twoDaysAgo = (datetime.date.today() - datetime.timedelta(2)).strftime("%a%m%d%Y")

  dates = [today, yesterday, twoDaysAgo]
  rows = []
  for date in dates:
    day = date[:3]
    try:
      cursor.execute('SELECT id, rackNum, col, row FROM ' +date+ " WHERE accn == '"+accn+"' ORDER BY id DESC")
    except sqlite3.OperationalError:
      print "SQLite DB locked"
    else:
      for thing in cursor:
        # print thing
        rows.append(thing + (day,))
#  db.close()
  return rows


def findAll():
#  print accn
  db = sqlite3.connect('racks.db')
  cursor = db.cursor()
  today = newDay()
  yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime("%a%m%d%Y")
  twoDaysAgo = (datetime.date.today() - datetime.timedelta(2)).strftime("%a%m%d%Y")

  dates = [twoDaysAgo, yesterday, today]
  rows = []
  setRows = orderedset.OrderedSet()
  for date in dates:
    #Getting the Day string
    day = date[:3]
    try:
      cursor.execute('SELECT id, accn FROM ' +date+ " ORDER BY id ASC")
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
  today = newDay()
  loc = locateNext()
  db = sqlite3.connect('racks.db')
  date = strftime("%m-%d", gmtime())
  timeFiled = strftime("%Y-%m-%d %H:%M:%S", gmtime())
  cursor = db.execute("INSERT INTO " + today  + " (accn, rackNum, date, timeFiled, col, row) VALUES(?,?,?,?,?,?)", (accn, loc[0], date, timeFiled, loc[1], loc[2]))
  db.commit()
  db.close()

def testDB():
  test = 0

  accn = "012546308014"
  while test < 10:
    fileAccn(accn)
    test +=1
  db = sqlite3.connect('racks.db')
  cursor.execute("""CREATE TABLE IF NOT EXISTS tube_data (id INTEGER PRIMARY KEY, accn TEXT, rackNum TEXT, date TEXT, timeFiled TEXT, col TEXT, row TEXT)""")
  today = datetime.datetime.now().strftime("%a%m%d%Y")
  cursor = db.execute('SELECT max(id) FROM ' + today)
  max_id = cursor.fetchone()[0]

if __name__ == '__main__':
  testDB()
  fileAccn("test")
  pprint(findAccn("test"))



