rapido.souper
=============

    >>> from zope.interface import implements, alsoProvides, implementer, Interface
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

    >>> from rapido.core.interfaces import IDatabasable, IStorage

Create object which can store soup data:

    >>> from node.ext.zodb import OOBTNode
    >>> from node.base import BaseNode
    >>> from zope.annotation.interfaces import IAttributeAnnotatable
    >>> class SiteNode(OOBTNode):
    ...    implements(IAttributeAnnotatable)
    >>> root = SiteNode()

Create a persistent object that will be adapted as a rapido db:

    >>> class DatabaseNode(BaseNode):
    ...    implements(IAttributeAnnotatable, IDatabasable)
    ...    def __init__(self, uid, root):
    ...        self.uid = uid
    ...        self['root'] = root
    ...
    ...    @property
    ...    def root(self):
    ...        return self['root']
    >>> root['mydb'] = DatabaseNode(1, root)
    >>> db_obj = root['mydb']
    >>> storage = IStorage(db_obj)
    >>> storage.initialize()

Let's create a document:

    >>> doc = storage.create()
    >>> uid = doc.uid()
    >>> doc.set_item('song', 'Where is my mind?')
    >>> storage.get(uid).has_item('song')
    True
    >>> doc.get_item('song')
    'Where is my mind?'
    >>> doc.set_item('docid', "doc_1")
    >>> doc.items()
    [('song', 'Where is my mind?'), ('docid', 'doc_1')]
    >>> storage.reindex(doc)
    >>> len([doc for doc in storage.search('docid=="doc_1"')])
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

Delete items or document:

    >>> doc.remove_item('song')
    >>> doc.has_item('song')
    False
    >>> list(doc for doc in storage.documents())
    [<rapido.souper.document.DocumentRecord object at ...>]
    >>> storage.delete(doc)
    >>> list(storage.documents())
    []