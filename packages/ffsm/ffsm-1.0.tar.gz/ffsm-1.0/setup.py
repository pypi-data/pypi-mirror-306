from setuptools import setup, find_packages

setup(
    name='ffsm',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ffsm=ffsm.mover:cli',
        ],
    },
    author="Chowdhury Faizal Ahammed",
    description="A utility to rename files with wildcard support",
    keywords="ffsm"
)
