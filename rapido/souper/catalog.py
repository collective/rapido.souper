from souper.interfaces import ICatalogFactory
from souper.soup import NodeAttributeIndexer
from zope.interface import implementer
from repoze.catalog.catalog import Catalog
from repoze.catalog.indexes.field import CatalogFieldIndex

@implementer(ICatalogFactory)
class CatalogFactory(object):

    def __call__(self, context=None):
        catalog = Catalog()
        docid_indexer = NodeAttributeIndexer('docid')
        catalog[u'docid'] = CatalogFieldIndex(docid_indexer)
        return catalog