from setuptools import setup

APP = ['main.py']


OPTIONS = {'argv_emulation': True,
           'iconfile': './PyBrowse.icns',
           'includes': ['six', 'packaging', 'packaging.version',
                        'packaging.specifiers', 'packaging.requirements'],
           'plist': {
                'CFBundleIdentifier': "com.moosystems.pybrowse",
                'CFBundleName': "PyBrowse",
                'CFBundleVersion': '1001',
                'CFBundleShortVersionString': '1.0',
               'NSHumanReadableCopyright': 'Copyright 2016 moosystems'
            }}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app', ]
)
