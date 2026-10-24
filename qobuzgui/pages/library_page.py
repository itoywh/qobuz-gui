from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qobuzgui.i18n import t


class LibraryPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(QLabel(f"<h2>{t('page.library')}</h2>"))
        layout.addWidget(
            QLabel(
                "骨架页：读取 qobuz-dl 下载数据库，展示已下专辑，支持打开目录/重下。"
            )
        )
        layout.addStretch(1)
