from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qobuzgui.i18n import t


class QueuePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(QLabel(f"<h2>{t('page.queue')}</h2>"))
        layout.addWidget(
            QLabel(
                "骨架页：下载任务列表（进度条/状态/暂停取消），下一轮由 QThread "
                "worker 通过 signals 回传进度并刷新。"
            )
        )
        layout.addStretch(1)
