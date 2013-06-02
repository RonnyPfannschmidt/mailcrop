from abc import ABCMeta, abstractmethod
from reprtools import FormatRepr


class Matcher(metaclass=ABCMeta):
    #@abstractmethod #XXX
    def match(self, message):
        pass

    @abstractmethod
    def to_imap(self):
        pass


class Header(Matcher):
    def __init__(self, header, substring):
        self.header = header
        self.substring = substring

    to_imap = FormatRepr('HEADER {header} "{substring}"')


class Simple(Matcher):
    def __init__(self, type_, contains):
        self.type = type_
        self.contains = contains

    to_imap = FormatRepr('{type} "{contains}"')


class OR(Matcher):
    def __init__(self, *matchers):
        self.matchers = matchers

    def to_imap(self):
        it = iter(self.matchers)
        res = next(it).to_imap()
        for other in it:
            res = 'OR {other} {res}'.format(
                other=other.to_imap(),
                res=res)
        return res


class Ml(OR):
    def __init__(self, ml):
        self.ml = ml
        super().__init__(
            Header('List-Post', ml),
            Simple('TO', ml),
            Simple('CC', ml),
        )

    __repr__ = FormatRepr('<Match ml {ml}>')
