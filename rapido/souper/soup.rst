rapido.souper
=============

    >>> from zope.interface import implements, alsoProvides, implementer, Interface
    >>> from zope.component import provideAdapter
    >>> from zope.configuration.xmlconfig import XMLConfig
    >>> import zope.component
    >>> XMLConfig("meta.zcml", zope.component)()
    >>> import zope.browserpage
    >>> XMLConfig("meta.zcml", zope.browserpage)()
    >>> import zope.annotation
    >>> XMLConfig("configure.zcml", zope.annotation)()
    >>> import rapido.core
    >>> XMLConfig("configure.zcml", rapido.core)()
    >>> import rapido.souper
    >>> XMLConfig("configure.zcml", rapido.souper)()

    >>> from rapido.core.interfaces import IRapidable, IStorage

Create object which can store soup data:

    >>> from rapido.souper.locator import StorageLocator
    >>> provideAdapter(StorageLocator, adapts=[Interface])
    >>> from node.ext.zodb import OOBTNode
    >>> from node.base import BaseNode
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> class SiteNode(OOBTNode):
    ...    implements(IAttributeAnnotatable)
    >>> root = SiteNode()

Create a persistent object that will be adapted as a rapido db:

    >>> from rapido.core.app import Context
    >>> class DatabaseNode(BaseNode):
    ...    implements(IAttributeAnnotatable, IRapidable)
    ...    def __init__(self, id, root):
    ...        self.id = id
    ...        self['root'] = root
    ...        self.context = Context()
    ...
    ...    def get_settings(self):
    ...        return ""
    ...
    ...    @property
    ...    def root(self):
    ...        return self['root']
    >>> root['mydb'] = DatabaseNode("test", root)
    >>> db_obj = root['mydb']
    >>> storage = IStorage(db_obj)
    >>> storage.initialize()

Let's create a record:

    >>> doc = storage.create()
    >>> uid = doc.uid()
    >>> doc['song'] = 'Where is my mind?'
    >>> 'song' in doc
    True
    >>> doc['song']
    'Where is my mind?'
    >>> doc['id'] = "doc_1"
    >>> doc.items()
    {'id': 'doc_1', 'song': 'Where is my mind?'}
    >>> [key for key in doc]
    ['song', 'id']
    >>> storage.reindex(doc)
    >>> len([doc for doc in storage.search('id=="doc_1"')])
    1

We can retrieve record:
    >>> storage.get(uid)['song']
    'Where is my mind?'
    >>> storage.get(999) is None
    True

Add indexes:

    >>> storage.create_index("band", "field")
    >>> doc['band'] = "Pixies"
    >>> len([doc for doc in storage.search('band=="Pixies"')])
    0
    >>> storage.reindex()
    >>> len([doc for doc in storage.search('band=="Pixies"')])
    1
    >>> storage.create_index("song", "text")
    >>> storage.reindex(doc)
    >>> len([doc for doc in storage.search('"mind" in song')])
    1

Delete items or record:

    >>> del doc['song']
    >>> 'song' in doc
    False
    >>> list(doc for doc in storage.records())
    [<rapido.souper.record.Record object at ...>]
    >>> storage.delete(doc)
    >>> list(storage.records())
    []

Reindex, rebuild, clear
    >>> doc1 = storage.create()
    >>> doc1['song'] = 'ABC'
    >>> doc2 = storage.create()
    >>> doc2['song'] = 'Thriller'
    >>> len([doc for doc in storage.search('song=="ABC"')])
    0
    >>> storage.reindex()
    >>> len([doc for doc in storage.search('song=="ABC"')])
    1
    >>> doc2['style'] = ['Pop',]
    >>> storage.rebuild()
    >>> storage.indexes
    [u'id']
    >>> storage.create_index("style", "keyword")
    >>> storage.reindex()
    >>> len([doc for doc in storage.search("style in any(['Pop', 'Rock'])")])
    1
    >>> storage.clear()
    >>> list(storage.records())
    []
