from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel

from qobuzgui.i18n import t


class SearchPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(QLabel(f"<h2>{t('page.search')}</h2>"))
        layout.addWidget(
            QLabel(
                "骨架页：搜索框 + 类型分段控件 + 结果列表将在下一轮接入 "
                "QobuzDL.search_by_type()。"
            )
        )
        layout.addStretch(1)
