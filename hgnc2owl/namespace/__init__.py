from typing import List
from rdflib.term import URIRef, Variable, _is_valid_uri


class Namespace(str):
    """
    Utility class for quickly generating URIRefs with a common prefix
    >>> from rdflib.namespace import Namespace
    >>> n = Namespace("http://example.org/")
    >>> n.Person # as attribute
    rdflib.term.URIRef('http://example.org/Person')
    >>> n['first-name'] # as item - for things that are not valid python identifiers
    rdflib.term.URIRef('http://example.org/first-name')
    >>> n.Person in n
    True
    >>> n2 = Namespace("http://example2.org/")
    >>> n.Person in n2
    False
    """

    def __new__(cls, value):
        try:
            rt = str.__new__(cls, value)
        except UnicodeDecodeError:
            rt = str.__new__(cls, value, "utf-8")
        return rt

    @property
    def title(self):
        # Override for DCTERMS.title to return a URIRef instead of str.title method
        return URIRef(self + "title")

    def term(self, name):
        # need to handle slices explicitly because of __getitem__ override
        return URIRef(self + (name if isinstance(name, str) else ""))

    def __getitem__(self, key):
        return self.term(key)

    def __getattr__(self, name):
        if name.startswith("__"):  # ignore any special Python names!
            raise AttributeError
        return self.term(name)

    def __repr__(self):
        return f"Namespace({super().__repr__()})"

    def __contains__(self, ref):
        """Allows to check if a URI is within (starts with) this Namespace.
        >>> from rdflib import URIRef
        >>> namespace = Namespace('http://example.org/')
        >>> uri = URIRef('http://example.org/foo')
        >>> uri in namespace
        True
        >>> person_class = namespace['Person']
        >>> person_class in namespace
        True
        >>> obj = URIRef('http://not.example.org/bar')
        >>> obj in namespace
        False
        """
        return ref.startswith(self)  # test namespace membership with "ref in ns" syntax


class DefinedNamespaceMeta(type):
    """
    Utility metaclass for generating URIRefs with a common prefix
    """

    _NS: Namespace
    _warn: bool = True
    _fail: bool = False  # True means mimic ClosedNamespace
    _extras: List[str] = []  # List of non-pythonesque items
    _underscore_num: bool = False  # True means pass "_n" constructs

    def __getitem__(cls, name, default=None):
        name = str(name)
        if str(name).startswith("__"):
            return super().__getitem__(name, default)
        if (cls._warn or cls._fail) and not name in cls:
            if cls._fail:
                raise AttributeError(f"term '{name}' not in namespace '{cls._NS}'")
            else:
                warnings.warn(
                    f"Code: {name} is not defined in namespace {cls.__name__}",
                    stacklevel=3,
                )
        return cls._NS[name]

    def __getattr__(cls, name):
        return cls.__getitem__(name)

    def __repr__(cls):
        return f'Namespace("{cls._NS}")'

    def __str__(cls):
        return str(cls._NS)

    def __add__(cls, other):
        return cls.__getitem__(other)

    def __contains__(cls, item):
        """Determine whether a URI or an individual item belongs to this namespace"""
        item_str = str(item)
        if item_str.startswith("__"):
            return super().__contains__(item)
        if item_str.startswith(str(cls._NS)):
            item_str = item_str[len(str(cls._NS)) :]
        return any(
            item_str in c.__annotations__
            or item_str in c._extras
            or (cls._underscore_num and item_str[0] == "_" and item_str[1:].isdigit())
            for c in cls.mro()
            if issubclass(c, DefinedNamespace)
        )


class DefinedNamespace(metaclass=DefinedNamespaceMeta):
    """
    A Namespace with an enumerated list of members.
    Warnings are emitted if unknown members are referenced if _warn is True
    """

    def __init__(self):
        raise TypeError("namespace may not be instantiated")

from hgnc2owl.namespace._HGNC import HGNC
from hgnc2owl.namespace._OBO import OBO
from hgnc2owl.namespace._OBOINOWL import OBOINOWL