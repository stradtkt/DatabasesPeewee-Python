import datetime
import sys
import os
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


def clear():
    os.system('clear')



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


def view_entries(search_query=None):
    """View entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())
    if search_query:
        entries = entries.where(Entry.content.contains(search_query))
    for entry in entries:
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %H:%M%p")
        print(timestamp)
        print("="*len(timestamp))
        print(entry.content)
        print("n) next entry")
        print("d) delete entry")
        print("q) return to the main menu")
        next_action = input('Action: [Ndq] ').lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search entries for a string"""
    view_entries(input('Search query:  '))
        
    
def delete_entry(entry):
    """Delete an entry"""
    if input('Are you sure? [yN]').lower == 'y':
        entry.delete_instance()
        print('Entry deleted!')

menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
])

if __name__ == '__main__':
    initialize()
    menu_loop()