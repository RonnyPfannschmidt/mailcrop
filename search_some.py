from mailcrop.imap import connect
from mailcrop.matching import Ml, OR


matchers = (
    Ml('testing-in-python@'),
    Ml('python-ideas@')
)
imap = connect(command='ssh us ./bin/imap')
print(imap.capabilities)
imap.select()
for matcher in matchers:
    print(matcher.to_imap())
    result = imap.search(matcher)
    print(matcher, result)
    copy_result = imap.copy(result, 'test2')
    import pdb
    pdb.set_trace()
    print(copy_result)
