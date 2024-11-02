from sympy import Basic, cacheit, Expr


class Application(Basic):
    """
    Base class for applied functions.
    """

    @cacheit
    def __new__(cls, *args):
        evaluated = cls.eval(*args)
        if evaluated is not None:
            return evaluated

    @classmethod
    def eval(cls, *args):
        """
        Returns a canonical form of cls applied to arguments args.

        Explanation
        ===========

        The ``eval()`` method is called when the class ``cls`` is about to be
        instantiated and it should return either some simplified instance
        (possible of some other class), or if the class ``cls`` should be
        unmodified, return None.
        """
        return

    @property
    def func(self):
        return self.__class__


class Function(Application, Expr):
    r"""
    Base class for applied mathematical functions
    """

    pass
