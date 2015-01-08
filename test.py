#!/usr/bin/env python
from pprint import pprint
from CodernityDB.database import Database
from CodernityDB.hash_index import HashIndex


class WithXIndex(HashIndex):

    def __init__(self, *args, **kwargs):
        kwargs['key_format'] = 'I'
        super(WithXIndex, self).__init__(*args, **kwargs)

    def make_key_value(self, data):
        a_val = data.get("x")
        if a_val is not None:
            return a_val, None
        return None

    def make_key(self, key):
        return key


def main():
    db = Database('/home/pi/tubesorter/test.db')
    db.create()
    x_ind = WithXIndex(db.path, 'x')
    db.add_index(x_ind)

    for x in xrange(100):
        db.insert(dict(x=x))

    for y in xrange(100):
        db.insert(dict(y=y))

    stuff = db.get('x', 10, with_doc=True)
    pprint(stuff)
    print db.count(db.all, 'id')
    print db.count(db.all, 'x')

if __name__ == '__main__':
    main()