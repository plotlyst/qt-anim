from pathlib import Path

from setuptools import setup, find_packages

HERE = Path(__file__).parent.absolute()
with (HERE / 'README.md').open('rt') as fh:
    LONG_DESCRIPTION = fh.read().strip()

REQUIREMENTS: dict = {
    'core': [
        'qtpy',
    ],
    'test': [
        'pytest==6.2.4',
        'pytest-qt==4.0.2',
        'pytest-cov==2.12.1',
    ],
    'dev': [
        'qt-handy'
    ],
    'doc': [
    ],
}

setup(
    name='qt-anim',
    version='0.1.0',

    author='Zsolt Kovari',
    author_email='',
    description='Qt Property Animations',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='',

    packages=find_packages(),
    python_requires='>=3.6, <4',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],

    install_requires=REQUIREMENTS['core'],
    extras_require={
        **REQUIREMENTS,
        'dev': [req
                for extra in ['dev', 'test', 'doc']
                for req in REQUIREMENTS.get(extra, [])],
        # The 'all' extra is the union of all requirements.
        'all': [req for reqs in REQUIREMENTS.values() for req in reqs],
    },
)
