import pymongo
import sys
import datetime
from pprint import pprint
from pymongo import MongoClient
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

    # accn_seed = {"accn": "14-123-1234",
    #     "rack": 1,
    #     "row": 1,
    #     "column":1,
    #     "date": datetime.datetime.utcnow()}

class database:
  def __init__(self):
    self.db   = MongoClient().test_database
    # self.db.drop_database
    self.accn_table = self.db.accn_table
    self.next_column = 1
    self.next_row = 1
    self.rack_number = 1
    self.str_day = ''
    self.last_filed   = self.accn_table.find().limit(1).sort([("_id", pymongo.DESCENDING)])[0]
    print self.accn_table.find_one()
    self.next_position()
  def next_position(self):
    if self.last_filed == None:
      self.date         = datetime.datetime.today().date()
      self.str_day      = datetime.datetime.now().strftime("%A")
      self.rack_number  = 1
      self.next_row     = 1
      self.next_column  = 1
    else:
      if self.last_filed['column'] == 6 and self.last_filed['row'] == 12:
        self.next_column  =   1
        self.next_row     =   1
        self.rack_number  +=  1
      elif self.last_filed['column'] == 6 and self.last_filed['row'] != 12:
        self.next_column  =   1
        self.next_row     +=  1
      elif self.last_filed['column'] != 6:
        self.next_column += 1

    next_pos_dict = { 'rack': self.str_day + '-' + str(self.rack_number),
                      'row':  1,
                      'column':  1,
                    }
    pprint(next_pos_dict)
    return next_pos_dict

  def locate_accn(self, accn):
    print self.date
  def file_accn(self, accn):
	insert_accn = {'accn':accn,
			'rack': self.rack_number,
			'row': self.next_row,
			'column': self.next_column,
			'date': datetime.datetime.utcnow()}
	pprint (insert_accn)

	self.accn_table.insert(insert_accn)
	self.next_position()	



# posts = db.posts
# post_id = posts.insert(post)
# post_id
# db.collection_names()
# wholedb = posts.find()
# for item in wholedb:
#         pprint(item)
# print "just one"
# pprint(posts.find_one())
# print 'last five sorted'
# sorted = posts.find().sort({$natural:-1}).limit(1)
# for item in sorted:
#   pprint(item)








if __name__ == '__main__':


  accn_seed = {"accn": "14-123-1234",
    "rack": 1,
    "row": 1,
    "column":1,
    "date": datetime.datetime.utcnow()}


  database = database()
  database.accn_table.insert(accn_seed)
  x = 0
  while x < 100:
	print x
  	database.file_accn(str(x))
	x += 1

  pprint(database.__dict__)


# def getTables():
#   conn = sqlite3.connect("racks.db")
#   tables = conn.cursor()
#   tables.execute('select name from sqlite_master where type=\'table\'')
#   rows = []
#   for row in tables:
#     rows.append(row)
#   conn.close()
#   return rows
# getTables()


# def newDay():
#   tables = getTables()
#   needNewDay = True
#   today = datetime.datetime.now().strftime("%a%m%d%Y")
#   for table in tables:
#     if table == today:
#       needNewDay = False
#   if not needNewDay:
#     return today  
#   db = sqlite3.connect('racks.db')
#   cursor = db.cursor()
#   day = datetime.datetime.now().strftime("%A")
#   cursor.execute("""CREATE TABLE IF NOT EXISTS """ + today + """(id INTEGER PRIMARY KEY, accn TEXT, rackNum TEXT, date TEXT, timeFiled TEXT, col TEXT, row TEXT)""")
#   db.close()
#   return today
# newDay()


# def lastFiled():
#   today = str(newDay())
#   db = sqlite3.connect('racks.db')
#   cursor = db.execute('SELECT max(id) FROM ' + today)
#   max_id = cursor.fetchone()[0]
#   if max_id is None:
#     return None
#   else:
#     cursor = db.execute('SELECT rackNum, col, row, accn FROM ' + today + ' where id is ' + str(max_id))
#     lastFiled = cursor.fetchone()
#     return lastFiled

# def locateNext():
#   today = str(newDay())
#   db = sqlite3.connect('racks.db')
#   cursor = db.execute('SELECT max(id) FROM ' + today)
#   max_id = cursor.fetchone()[0]
#   if max_id is None:
#     rackNum = 1
#     col = 0
#     row = 1
#   else:
#     cursor = db.execute('SELECT rackNum, col, row FROM ' + today + ' where id is ' + str(max_id))
#     lastRow = cursor.fetchone()
#     rackNum = int(lastRow[0])
#     col = int(lastRow[1])
#     row = int(lastRow[2])
#   if col == 6 and row == 12:
#     col = 1
#     row = 1
#     rackNum += 1
#   elif col == 6 and row != 12:
#     col = 1
#     row += 1
#   elif col != 6:
#     col += 1
#   nextSpot = [str(rackNum), str(col), str(row), today[:3]]
#   db.close()
#   return nextSpot
  
# def tuple_without(original_tuple, element_to_remove):
#     new_tuple = []
#     for s in list(original_tuple):
#         if not s == element_to_remove:
#             new_tuple.append(s)
#     return tuple(new_tuple)
  
# def findAccn(accn):
#   db = sqlite3.connect('racks.db')
#   cursor = db.cursor()
#   today = newDay()
#   yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime("%a%m%d%Y")
#   twoDaysAgo = (datetime.date.today() - datetime.timedelta(2)).strftime("%a%m%d%Y")

#   dates = [today, yesterday, twoDaysAgo]
#   rows = []
#   for date in dates:
#     day = date[:3]
#     try:
#       cursor.execute('SELECT id, rackNum, col, row FROM ' +date+ " WHERE accn == '"+accn+"' ORDER BY id DESC")
#     except sqlite3.OperationalError:
#       print "SQLite DB locked"
#     else:
#       for thing in cursor:
#         # print thing
#         rows.append(thing + (day,))
# #  db.close()
#   return rows


# def findAll():
# #  print accn
#   db = sqlite3.connect('racks.db')
#   cursor = db.cursor()
#   today = newDay()
#   yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime("%a%m%d%Y")
#   twoDaysAgo = (datetime.date.today() - datetime.timedelta(2)).strftime("%a%m%d%Y")

#   dates = [twoDaysAgo, yesterday, today]
#   rows = []
#   setRows = orderedset.OrderedSet()
#   for date in dates:
#     #Getting the Day string
#     day = date[:3]
#     try:
#       cursor.execute('SELECT id, accn FROM ' +date+ " ORDER BY id ASC")
#     except sqlite3.OperationalError:
#       print "SQLite DB locked"
#     else:
#       # setRows = orderedset.OrderedSet()
#       for item in cursor:
#         print item
#         setRows.add(item[1])
# #  db.close()
#   # setRows = set(rows)
#   for x in setRows:
#     print x
#   print "----"
#   while setRows:
#     rows.append(setRows.pop())
#   # rows.reverse()
#   return rows

# # findAll()


# def fileAccn(accn):
#   today = newDay()
#   loc = locateNext()
#   db = sqlite3.connect('racks.db')
#   date = strftime("%m-%d", gmtime())
#   timeFiled = strftime("%Y-%m-%d %H:%M:%S", gmtime())
#   cursor = db.execute("INSERT INTO " + today  + " (accn, rackNum, date, timeFiled, col, row) VALUES(?,?,?,?,?,?)", (accn, loc[0], date, timeFiled, loc[1], loc[2]))
#   db.commit()
#   db.close()


# #findAccn('012546308014')
# test  = 0
# def testDB():
#   test = 0
#   accn = "012546308014"
#   while test < 10:
#     fileAccn(accn)
#     test +=1
#   db = sqlite3.connect('racks.db')
#   today = datetime.datetime.now().strftime("%a%m%d%Y")
#   cursor = db.execute('SELECT max(id) FROM ' + today)
#   max_id = cursor.fetchone()[0]


# #testDB()


