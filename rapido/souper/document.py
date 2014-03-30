from zope.interface import implements
from copy import deepcopy

from rapido.core.interfaces import IRecordable

class DocumentRecord(object):
    implements(IRecordable)

    def __init__(self, context, database):
        self.context = context
        self.database = database

    def set_item(self, name, value):
        """ set an item value
        """
        self.context.attrs[name] = value

    def get_item(self, name):
        """ return an item value
        """
        if(self.has_item(name)):
            return deepcopy(self.context.attrs[name])

    def has_item(self, name):
        """ test if item exists
        """
        return self.context.attrs.has_key(name)

    def remove_item(self, name):
        """ remove an item
        """
        if self.context.attrs.has_key(name):
            del self.context.attrs[name]

    def uid(self):
        """ return internal identifier
        """
        return self.context.intid

    def items(self):
        """ return all items
        """
        return self.context.attrs.items()