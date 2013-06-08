from setuptools import setup

setup(
    name='mailcrop',
    get_version_from_scm=True,
    packages=['testing', 'mailcrop'],
    url='',
    license='MIT',
    author='Ronny Pfannschmidt',
    author_email='',
    description='simple sorter to get emails into imap mailboxes',
    setup_requires=[
        'hgdistver',
    ],
)
