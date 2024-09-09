from setuptools import setup

setup(
    name="task-cli",
    version="1.0",
    py_modules=['cliinterface'],  # The name of your CLI file
    install_requires=[
        'click',  # Dependencies
    ],
    entry_points='''
        [console_scripts]
        task-cli=cliinterface:cli
    ''',
)
