import importlib

_CURRENT: dict = {}
_LANG = "zh_CN"


def init_i18n(lang: str) -> None:
    global _CURRENT, _LANG
    _LANG = lang
    try:
        module = importlib.import_module(f"qobuzgui.i18n.{lang}")
        _CURRENT = getattr(module, "STRINGS", {})
    except Exception:
        module = importlib.import_module("qobuzgui.i18n.zh_CN")
        _CURRENT = getattr(module, "STRINGS", {})
        _LANG = "zh_CN"


def set_lang(lang: str) -> None:
    init_i18n(lang)


def current_lang() -> str:
    return _LANG


def t(key: str, default: str = "") -> str:
    """按 key 取当前语言文案；缺失时回退中文，再缺失时回退 default/key。"""
    if key in _CURRENT:
        return _CURRENT[key]
    if default:
        return default
    # 回退到中文
    try:
        from qobuzgui.i18n import zh_CN
        if key in zh_CN.STRINGS:
            return zh_CN.STRINGS[key]
    except Exception:
        pass
    return key
