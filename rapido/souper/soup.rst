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
    >>> doc.set_item('song', 'Where is my mind?')
    >>> storage.get(uid).has_item('song')
    True
    >>> doc.get_item('song')
    'Where is my mind?'
    >>> doc.set_item('id', "doc_1")
    >>> doc.items()
    {'id': 'doc_1', 'song': 'Where is my mind?'}
    >>> storage.reindex(doc)
    >>> len([doc for doc in storage.search('id=="doc_1"')])
    1

Add indexes:

    >>> storage.create_index("band", "field")
    >>> doc.set_item('band', "Pixies")
    >>> len([doc for doc in storage.search('band=="Pixies"')])
    0
    >>> storage.reindex(doc)
    >>> len([doc for doc in storage.search('band=="Pixies"')])
    1
    >>> storage.create_index("song", "text")
    >>> storage.reindex(doc)
    >>> len([doc for doc in storage.search('"mind" in song')])
    1

Delete items or record:

    >>> doc.remove_item('song')
    >>> doc.has_item('song')
    False
    >>> list(doc for doc in storage.records())
    [<rapido.souper.record.Record object at ...>]
    >>> storage.delete(doc)
    >>> list(storage.records())
    []