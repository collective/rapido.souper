from zope.interface import implements
from zope.component import provideUtility
from souper.soup import get_soup, Record
from repoze.catalog.query import Eq

from rapido.core.interfaces import IStorage, IRecordable

from .catalog import CatalogFactory

class SoupStorage(object):
    implements(IStorage)

    def __init__(self, context):
        self.context = context
        self._soup = None

    def initialize(self):
        """ setup the storage
        """
        provideUtility(CatalogFactory(), name=self._get_id())
        self._soup = get_soup(self._get_id(), self.context)

    @property
    def soup(self):
        if not self._soup:
            self._soup = get_soup(self._get_id(), self.context)
        return self._soup

    def create(self):
        """ return a new document
        """
        record = Record()
        rid = self.soup.add(record)
        return IRecordable(self.soup.get(rid))

    def get(self, uid=None):
        """ return an existing document
        """
        record = self.soup.get(uid)
        if not record:
            return None
        return IRecordable(record)

    def save(self, doc):
        """ save a document
        """
        # the soup record stores item immediately
        pass

    def delete(self, doc):
        """ delete a document
        """
        del self.soup[doc.context]

    def search(self, query):
        """ search for documents
        """

    def _get_id(self):
        return "SOUP_" + str(hash(self.context))