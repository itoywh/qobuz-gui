from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QStackedWidget,
    QHBoxLayout,
)
from qobuzgui.i18n import t

from qobuzgui.pages.search_page import SearchPage
from qobuzgui.pages.url_page import UrlPage
from qobuzgui.pages.queue_page import QueuePage
from qobuzgui.pages.library_page import LibraryPage
from qobuzgui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("app_name"))
        self.resize(920, 600)
        self._build_ui()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.nav = QListWidget()
        self.nav.setFixedWidth(200)
        self.nav.addItem(t("nav.search"))
        self.nav.addItem(t("nav.url"))
        self.nav.addItem(t("nav.queue"))
        self.nav.addItem(t("nav.library"))
        self.nav.addItem(t("nav.settings"))
        self.nav.currentRowChanged.connect(self._switch_page)

        self.stack = QStackedWidget()
        self.pages = [
            SearchPage(),
            UrlPage(),
            QueuePage(),
            LibraryPage(),
            SettingsPage(),
        ]
        for p in self.pages:
            self.stack.addWidget(p)

        layout.addWidget(self.nav)
        layout.addWidget(self.stack, 1)
        self.nav.setCurrentRow(0)

    def _switch_page(self, row: int):
        if 0 <= row < len(self.pages):
            self.stack.setCurrentIndex(row)
