import datetime
import sys
from collections import OrderedDict
from peewee import *

db = SqliteDatabase("diary.db")

class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def initialize():
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    choice = None
    while choice != 'q':
        print('Enter q to quit')
        for key, value in menu.items():
            print('{}) {}'.format(key, value.__doc__))
        choice = input('Action: ').lower().strip()

        if choice in menu:
            menu[choice]()

def add_entry():
    """Add an entry"""
    print("Enter your entry press ctrl+d when finished")
    data = sys.stdin.read().strip()
    if data:
        if input('Save Entry? [Yn] ').lower() != 'n':
            Entry.create(content=data)
            print("Saved successfully")


def view_entries():
    """View entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    for entry in entries:
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %H:%M%p")
        print(timestamp)
        print("="*len(timestamp))
        print(entry.content)
        print("N) next entry")
        print("q) return to the main menu")
        next_action = input('Action: [Nq] ').lower().strip()
        if next_action == 'q':
            break

def delete_entry():
    """Delete an entry"""

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries)
])

if __name__ == '__main__':
    initialize()
    menu_loop()