import imaplib
from collections import namedtuple


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
        if isinstance(raw, bytes):
            super().__init__(map(int, raw.split(b' ')))
        else:
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
    "sanity wrapper around imaplib"
    def __init__(self, fsck_imap):
        self.fsck_imap = fsck_imap
        self.capabilities = set(fsck_imap.capabilities)
        assert 'UIDPLUS' in self.capabilities

    def select(self, mailbox='INBOX'):
        ok, result = self.fsck_imap.select(mailbox)
        ImapError.maybe_raise(ok, result)

    def _uid(self, command, *args):
        args = _args_to_imap(args)
        ok, result = self.fsck_imap.uid(command, *args)
        ImapError.maybe_raise(ok, result)
        return result

    def search(self, *args):
        result = self._uid('search', *args)
        return MessageList(*result)

    def copy(self, message_set, mailbox):
        result = self._uid('copy', message_set, mailbox)
        assert result == [None]
        data, = self.fsck_imap.untagged_responses.pop('COPYUID')
        val, ss, ts = data.split()
        return CopyResult(val, ss, ts)

    def uid_indirect_move(self, message_set, mailbox):
        return self._uid('copy', message_set, mailbox)
