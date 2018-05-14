from setuptools import setup, find_packages

setup(
    name='mara-cli',
    version='0.1',

    description="Mara cli app which calls the appropriate contributed subcommand.",

    install_requires=[
        'mara-config>=0.1',
        'click'
        ],

    dependency_links=[
        'git+https://github.com/mara/mara-config.git@master#egg=mara-config',
    ],

    extras_require={
        'test': ['pytest'],
    },

    packages=find_packages(),

    author='Mara contributors',
    license='MIT',

    entry_points={
        'console_scripts': [
            'mara = mara_cli.cli:main',
        ],
    },

)
