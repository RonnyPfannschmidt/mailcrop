import imaplib
from collections import namedtuple

imaplib.Commands['MOVE'] = ('SELECTED',)


def connect(*, command):
    """
    for now we only support imap by ssh using preauth
    """
    imap = imaplib.IMAP4_stream(command)
    assert imap.state == 'AUTH', 'only preauth supported atm'
    return Imap(imap)


def _to_imap(x):
    if hasattr(x, 'to_imap'):
        return x.to_imap()
    else:
        return x


def _args_to_imap(args):
    return list(map(_to_imap, args))


class MessageList(list):
    def __init__(self, raw):
        if not raw:
            raw = ()
        elif isinstance(raw, bytes):
            raw = map(int, raw.split(b' '))
        super().__init__(raw)

    def to_imap(self):
        assert self, 'empty messageset breaks'
        return ','.join(map(str, self))


class MessageSet(str):
    pass


CopyResult = namedtuple('CopyResult', [
    'target_uidvalidity',
    'source_set',
    'target_set',
])


class ImapError(Exception):
    @classmethod
    def maybe_raise(cls, ok, result):
        if ok != 'OK':
            raise cls(ok, result)


class Imap(object):
    """
    sanity wrapper around <imaplib>
    """

    def __init__(self, _imap: imaplib.IMAP4):
        self._imap = _imap
        self.capabilities = set(_imap.capabilities)
        self.untagged_responses = _imap.untagged_responses
        assert 'UIDPLUS' in self.capabilities

    def select(self, mailbox='INBOX'):
        ok, result = self._imap.select(mailbox)
        ImapError.maybe_raise(ok, result)

    def _uid(self, command, *args):
        args = _args_to_imap(args)
        ok, result = self._imap.uid(command, *args)
        ImapError.maybe_raise(ok, result)
        return result

    def search(self, *args):
        """
        do an imap search

        :param args: imap search parameters
        :return: MessageList of results
        """
        result = self._uid('search', *args)
        return MessageList(*result)

    def copy(self, message_set, mailbox):
        result = self._uid('copy', message_set, mailbox)
        assert result == [None]
        data, = self._imap.untagged_responses.pop('COPYUID')
        val, ss, ts = data.split()
        return CopyResult(val, ss, ts)

    def store(self, message_set, *args):
        #XXX result type
        return self._uid('store', message_set, *args)

    def add_flags(self, message_set, *flags):
        #XXX result parser
        return self.store(message_set, '+FLAG', flags)

    def selective_expunge(self, message_set):
        assert message_set
        #XXX: result type
        return self._uid('EXPUNGE', message_set)

    def indirect_move(self, message_set, mailbox):
        copy_result = self.copy(message_set, mailbox)
        store_result = self.add_flags(copy_result.source_set, '\\Deleted')
        self.selective_expunge(copy_result.source_set)
        return copy_result

    def direct_move(self, message_set, mailbox):
        result = self._uid('move', message_set, self._imap._quote(mailbox))

    def move(self, message_set, mailbox):
        assert 'MOVE' in self.capabilities
        return self.direct_move(message_set, mailbox)

    def apply_rules(self, rules):
        for rule in rules:
            rule.apply_mailbox(self)