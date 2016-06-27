from setuptools import setup, find_packages

setup(
    name='ticket',
    version='0.0.1',
    description='A simple way to keep your manager happy',
    author='mikeroll',
    author_email='scaryspiderpig@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ticket=ticket.ticket:cli'
        ]
    },
    install_requires=[
        "appdirs==1.4.0",
        "click==6.6",
        "PyYAML==3.11",
        "tabulate==0.7.5",
        "jira"
    ]
)
