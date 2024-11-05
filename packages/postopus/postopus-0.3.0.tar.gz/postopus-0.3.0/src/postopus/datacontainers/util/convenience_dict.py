class ConvenienceDict:
    """
    Base class with convenience access to a dictionary

    Inherit from this class to allow access to all entries in a dictionary
    directly as properties of the class. The name of this special dictionary is
    'data' and can be overridden by setting the value of '__dict_name__'.

    Example:

    >>> class Example(ConvenienceDict):
    >>>     pass
    >>> e = Example({'a': 1, 'b': 2})
    >>> print(e.a, e.b)
    1 2
    >>> e.data['x'] = 4
    >>> print(e.x)
    4

    Using a different dictionary works as follows:
    >>> class Example(ConvenienceDict):
    >>>     __dict_name__ = 'systems'
    >>>     def __init__(self):
    >>>         super().__init__({'a': 1, 'b': 2})
    >>> e = Example()
    >>> print(e.a, e.b)
    1 2
    """

    __dict_name__ = "data"

    def __init__(self, data=None):
        data = data if data else {}
        setattr(self, self.__class__.__dict_name__, data)

    def __getattr__(self, name):
        if name in getattr(self, self.__class__.__dict_name__):
            return getattr(self, self.__class__.__dict_name__)[name]
        else:
            raise AttributeError

    def __setattr__(self, attribute, value):
        if attribute == self.__class__.__dict_name__ or attribute not in getattr(
            self, self.__class__.__dict_name__
        ):
            super().__setattr__(attribute, value)
        else:
            getattr(self, self.__class__.__dict_name__)[attribute] = value

    def __dir__(self):
        return dir(self.__class__) + list(
            getattr(self, self.__class__.__dict_name__).keys()
        )
