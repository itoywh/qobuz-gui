import os
import json

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QFormLayout,
    QGroupBox,
)

from qobuzgui.i18n import t, set_lang, current_lang

CONFIG_DIR = os.path.expanduser("~/Library/Application Support/QobuzDownloader")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(QLabel(f"<h2>{t('page.settings')}</h2>"))

        form = QFormLayout()
        self.lang = QComboBox()
        self.lang.addItem(t("lang.zh"), "zh_CN")
        self.lang.addItem(t("lang.en"), "en_US")
        idx = self.lang.findData(current_lang())
        if idx >= 0:
            self.lang.setCurrentIndex(idx)
        self.lang.currentIndexChanged.connect(self._on_lang)
        form.addRow(t("settings.language"), self.lang)

        box = QGroupBox("General")
        box.setLayout(form)
        layout.addWidget(box)

        self.hint = QLabel("")
        layout.addWidget(self.hint)
        layout.addStretch(1)

    def _on_lang(self, index: int):
        lang = self.lang.itemData(index)
        set_lang(lang)
        self._save_lang(lang)
        self.hint.setText(f"语言已切换为 {lang}，重启后全量生效（MVP）。")

    def _save_lang(self, lang: str):
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            cfg = {}
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
            cfg["language"] = lang
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
