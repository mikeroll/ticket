from setuptools import setup, find_packages

setup(
    name='ticket',
    version='0.0.1',
    description='Dead simple way to make your manager happy',
    author='mikeroll',
    author_email='scaryspiderpig@gmail.com',
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ticket=ticket:cli'
        ]
    }
)
