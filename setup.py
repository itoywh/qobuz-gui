from setuptools import setup

APP_NAME = "Qobuz Downloader"
APP = ["main.py"]
DATA_FILES = []

OPTIONS = {
    # Do NOT use packages=["PySide6"] — that copies the ENTIRE PySide6 wheel
    # (all Qt frameworks + all plugins, ~300MB of unused stuff).
    # Instead list only the Qt modules we actually import; py2app pulls in
    # just their transitive framework deps, and scripts/trim_app.sh finishes
    # the job by deleting any framework dirs nothing references.
    "argv_emulation": False,
    "packages": ["qobuz_dl"],
    "includes": [
        "PySide6",
        "PySide6.QtCore",
        "PySide6.QtWidgets",
        "PySide6.QtGui",
        "PySide6.QtNetwork",
        "PySide6.QtSvg",
    ],
    "excludes": [
        # Pure-Python stdlib bits we never ship
        "tkinter", "unittest", "pydoc", "doctest",
        "test", "idlelib", "pydoc_data", "ensurepip",
        "setuptools", "pip", "distutils",
    ],
    "optimize": 2,  # strip docstrings/asserts from bundled bytecode
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
