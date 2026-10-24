from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qobuzgui.i18n import t


class UrlPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(QLabel(f"<h2>{t('page.url')}</h2>"))
        layout.addWidget(
            QLabel(
                "骨架页：多链接文本框 + 拖入 .txt + last.fm 歌单 + 选项 + 开始下载，"
                "下一轮接入 QobuzDL.download_list_of_urls()/handle_url()。"
            )
        )
        layout.addStretch(1)
