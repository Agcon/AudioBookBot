from setuptools import setup
from pkg_resources import parse_requirements


with open('requirements.txt') as f:
    requirements = [str(req) for req in parse_requirements(f)]

setup(
    name='AudioBookBot',
    version='1.0.0',
    author='Agcon, pr0maxxx, MrGreys0n',
    description='Converts text from books into audio',
    packages=['main'],
    install_requires=requirements,

    extras_require={
        'docs': [
            'sphinx',
            'sphinx_rtd_theme'
        ]
    },
    entry_points={
        'console_scripts': [
            'audiobookbot = main.audiobookbot:main'
        ]
    }
)
