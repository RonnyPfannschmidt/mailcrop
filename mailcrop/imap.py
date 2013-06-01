import imaplib

def connect(*, command):
    """
    for now we only support imap by ssh using preauth
    """
    imap = imaplib.IMAP4_stream(command)
    assert imap.state == 'AUTH', 'only preauth supported atm'
    return imap
