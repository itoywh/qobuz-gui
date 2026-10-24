import sys
import os

from PySide6.QtWidgets import QApplication

from qobuzgui.i18n import init_i18n, t
from qobuzgui.login_dialog import LoginDialog
from qobuzgui.main_window import MainWindow

CONFIG_DIR = os.path.expanduser("~/Library/Application Support/QobuzDownloader")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


def load_language() -> str:
    """默认中文(简体)，优先读取已保存的 config.language。"""
    lang = "zh_CN"
    try:
        if os.path.exists(CONFIG_FILE):
            import json
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                cfg = json.load(f)
            lang = cfg.get("language", "zh_CN")
    except Exception:
        pass
    return lang


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName(t("app_name"))

    init_i18n(load_language())

    # 骨架阶段：始终弹出登录窗（真实 get_tokens()+initialize_client 在下一轮接入）
    login = LoginDialog()
    if login.exec() != LoginDialog.Accepted:
        return 0

    win = MainWindow()
    win.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
