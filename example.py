import argparse
from mailcrop.imap import connect
from mailcrop.rules import MailingList as ML, Rule as R


def pyML(name, suffix=None):
    if suffix is None:
        suffix = name
    target = 'Mailing Listen.python.' + suffix
    address = name + '@python.org'
    return ML(name, address, target)


def main(options, command, rules):
    imap = connect(command=command)
    imap.select(options.mailbox)
    imap.apply_rules(rules)


def MF(name):
    return 'Mailing Listen.' + name


rules = [
    pyML('pypy-dev'),
    pyML('python-ideas', 'ideas'),
    pyML('distutils-sig', 'distutils'),
    pyML('code-quality'),
    pyML('pytest-dev', 'dev'),

    ML('TIP', 'testing-in-python@lists.idyll.org', MF('python.testing')),
]

parser = argparse.ArgumentParser()
parser.add_argument('mailbox', nargs='?',
                    default='INBOX')
parser.add_argument('--command', default='~/bin/imap')

if __name__ == '__main__':
    options = parser.parse_args()
    main(options, options.command, rules)
