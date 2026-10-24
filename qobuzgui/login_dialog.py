from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QCheckBox,
)
from PySide6.QtCore import Qt

from qobuzgui.i18n import t


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(t("login.title"))
        self.resize(400, 360)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        subtitle = QLabel(t("login.subtitle"))
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        layout.addWidget(QLabel(t("login.email")))
        self.email = QLineEdit()
        self.email.setPlaceholderText("you@example.com")
        layout.addWidget(self.email)

        layout.addWidget(QLabel(t("login.password")))
        self.pwd = QLineEdit()
        self.pwd.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.pwd)

        self.show_btn = QPushButton(t("login.show"))
        self.show_btn.setCheckable(True)
        self.show_btn.clicked.connect(self._toggle_show)
        row = QHBoxLayout()
        row.addWidget(self.show_btn)
        row.addStretch(1)
        layout.addLayout(row)

        self.keychain = QCheckBox(t("login.keychain"))
        layout.addWidget(self.keychain)

        self.signin = QPushButton(t("login.signin"))
        self.signin.clicked.connect(self._signin)
        layout.addWidget(self.signin)

        self.status = QLabel(t("login.status_idle"))
        layout.addWidget(self.status)

    def _toggle_show(self, checked: bool):
        self.pwd.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)

    def _signin(self):
        # 骨架：仅本地非空校验。真实 get_tokens()+initialize_client 在下一轮接入。
        if not self.email.text().strip() or not self.pwd.text():
            self.status.setText(t("login.status_empty"))
            return
        self.status.setText(t("login.status_ok"))
        self.accept()
