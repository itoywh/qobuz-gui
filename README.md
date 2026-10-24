# Qobuz Downloader (macOS GUI)

基于 [vitiko98/qobuz-dl](https://github.com/vitiko98/qobuz-dl) 的 macOS 图形界面封装。
直接调用 `qobuz_dl.core.QobuzDL` 模块（非套命令行壳），用 PySide6 实现原生 macOS 外观，
`py2app` 打包为双击即用的 `.app`。

## 功能（规划）

- 登录（Qobuz 账号 + 密码，API key 由程序自动抓取）
- 搜索（按专辑/曲目/艺人/歌单）
- 按 URL 下载（单/多链接、拖入 `.txt`、last.fm 歌单）
- 下载队列（实时进度、暂停/取消）
- 本地曲库（读取 qobuz-dl 下载数据库）
- 设置（音质、并发、命名格式、代理出口、语言）
- 语言：默认中文(简体)，可选 English

## 技术栈

- PySide6（LGPL，Qt 原生 macOS 外观）
- py2app（打包 `.app`）
- 与 qobuz-dl 共用 config / 下载数据库，CLI 与 GUI 状态互通

## 构建（由 GitHub Actions 完成，无需本地编译）

每次 push 到 `main` 会触发 `macOS-latest` runner 上的构建，产物 `.app` 作为
**Build macOS .app** workflow 的 artifact 提供下载。

本地如需自建：

```bash
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
./venv/bin/python setup.py py2app
# 产物位于 dist/Qobuz Downloader.app
```

## 状态

当前为最小骨架（v0.1.0）：UI 结构 + i18n + 登录窗 + py2app/CI 工具链已就绪，
真实 qobuz-dl 集成（搜索/下载/进度）在下一轮实现。
