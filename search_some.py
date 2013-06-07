from mailcrop.imap import connect
from mailcrop.rules import MailingList as ML, Rule as R


rules = [
    ML('pypy-dev', 'pypy-dev@python.org', "Mailing Listen.python.pypy-dev"),
    ML('python-ideas','python-ideas@python.org','Mailing Listen.python.ideas'),
    ML('couchdb-dev','dev@couchdb.apache.org','Mailing Listen.couch-dev'),
    ML('distutils sig', 'distutils-sig@python.org', 'Mailing Listen.python.distutils'),
    ML('hg dev','mercurial-devel@selenic.com','Mailing Listen.mercurial-devel'),
]

imap = connect(command='ssh us ./bin/imap')
imap.select()
imap.apply_rules(rules)
