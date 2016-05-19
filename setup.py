from setuptools import setup

setup(
    name='ticket',
    version='0.0.1',
    description='A simple way to keep your manager happy',
    author='mikeroll',
    author_email='scaryspiderpig@gmail.com',
    license='MIT',
    py_modules=['ticket'],
    entry_points={
        'console_scripts': [
            'ticket=ticket:cli'
        ]
    },
    install_requires=[
        "appdirs==1.4.0",
        "click==6.6",
        "jira==1.0.3",
        "oauthlib==1.1.1",
        "PyYAML==3.11",
        "requests-oauthlib==0.6.1",
        "requests-toolbelt==0.6.2",
        "requests==2.10.0",
        "six==1.10.0",
        "tabulate==0.7.5",
        "tlslite==0.4.9",
    ]
)
