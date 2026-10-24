from setuptools import setup

APP_NAME = "Qobuz Downloader"
APP = ["main.py"]
DATA_FILES = []

OPTIONS = {
    "argv_emulation": False,
    "packages": ["PySide6", "qobuz_dl"],
    "includes": [
        "PySide6.QtCore",
        "PySide6.QtWidgets",
        "PySide6.QtGui",
        "PySide6.QtNetwork",
    ],
    "excludes": ["tkinter", "unittest", "pydoc", "doctest"],
    "plist": {
        "CFBundleName": APP_NAME,
        "CFBundleDisplayName": APP_NAME,
        "CFBundleIdentifier": "com.itoywh.qobuzgui",
        "CFBundleVersion": "0.1.0",
        "CFBundleShortVersionString": "0.1.0",
        "LSMinimumSystemVersion": "11.0",
        "NSHighResolutionCapable": True,
    },
}

setup(
    name=APP_NAME,
    app=APP,
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
