from zope.interface import implements, alsoProvides
from zope.component import provideUtility, getMultiAdapter
from souper.soup import get_soup, Record
from souper.plone.interfaces import ISoupRoot
from souper.plone.locator import StorageLocator
from repoze.catalog.query import Eq

from rapido.core.interfaces import IStorage, IRecordable, IDatabase

from .catalog import CatalogFactory

class SoupStorage(object):
    implements(IStorage)

    def __init__(self, context):
        self.context = context
        provideUtility(CatalogFactory(), name=self._get_id())

    def initialize(self, root):
        """ setup the storage
        """
        alsoProvides(root, ISoupRoot)
        locator = StorageLocator(root)
        locator.storage(self._get_id())
        self._soup = get_soup(self._get_id(), root)

    @property
    def soup(self):
        if not hasattr(self, '_soup'):
            self._soup = get_soup(self._get_id(), self.context)
        return self._soup

    def create(self):
        """ return a new document
        """
        record = Record()
        rid = self.soup.add(record)
        return getMultiAdapter(
            (self.soup.get(rid), IDatabase(self.context)),
            IRecordable)

    def get(self, uid=None):
        """ return an existing document
        """
        record = self.soup.get(uid)
        if not record:
            return None
        return getMultiAdapter(
            (record, IDatabase(self.context)),
            IRecordable)

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
        return "rapido_%s" % (self.context.uid)