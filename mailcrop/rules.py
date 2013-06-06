from . import matching

class Rule(object):
    def __init__(self, name,*,matcher, target=None, flags=None):
        self.name = name
        self.matcher = matcher
        self.target = target
        self.flags = flags


    def apply_mailbox(self, imap):
        "apply this rule on the currently selected mailbox"
        messages = imap.search(self.matcher)
        if self.flags:
            imap.add_flags(messages, self.flags)
        if self.target:
            imap.move(messages, self.target)


class MailingList(Rule):
    def __init__(self, name, ml, target, *, flags=None):
        super.__init__(name,
                       matcher=matching.ML(name),
                       target=target,
                       flags=None)
