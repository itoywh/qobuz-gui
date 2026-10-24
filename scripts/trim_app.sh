#!/bin/bash
# Aggressively shrink a py2app PySide6 bundle down to what a plain
# QtWidgets (not QML) app actually needs.
#
# py2app's PySide6 recipe copies the ENTIRE wheel: every Qt framework, the
# whole Qt/qml tree, plugins, headers, translations. We keep only the small
# whitelist below and delete everything else by explicit name — no otool
# guesswork, so QtWebEngine/QtQuick/QtQml/etc. cannot sneak back in via a
# transitive .so link.
set -u

APP_DIR=$(ls -d dist/*.app 2>/dev/null | head -n1)
if [ -z "$APP_DIR" ]; then
  echo "ERROR: no built .app found in dist/" >&2
  exit 1
fi

PS="$APP_DIR/Contents/Resources/lib/python3.11/PySide6"

echo "== SIZE BEFORE =="
du -sh "$APP_DIR"

# --- Whitelists: ONLY these are kept; everything else is deleted. ----------
KEEP_SO="QtCore.so QtGui.so QtWidgets.so QtNetwork.so QtSvg.so"
KEEP_FRAMES="QtCore QtGui QtWidgets QtNetwork QtSvg QtConcurrent QtOpenGL QtOpenGLWidgets QtPrintSupport QtDBus QtXml"

# 1) We are a QtWidgets app, not QML -> drop the entire QML tree.
rm -rf "$PS/Qt/qml"
# 2) Drop dev-only headers and translations (not needed at runtime).
rm -rf "$PS/include"
rm -rf "$PS/Qt/translations"
rm -rf "$PS/Qt/resources" 2>/dev/null || true

# 3) Delete unused PySide6 Qt*.so modules (keep only the whitelist).
if [ -d "$PS" ]; then
  for m in "$PS"/Qt*.so; do
    [ -e "$m" ] || continue
    base=$(basename "$m")
    echo " $KEEP_SO " | grep -qw "$base" && continue
    echo "  rm module: $base"
    rm -f "$m"
  done
fi

# 4) Delete every Qt*.framework dir NOT in the whitelist.
while IFS= read -r d; do
  [ -d "$d" ] || continue
  name=$(basename "$d" .framework)
  if echo " $KEEP_FRAMES " | grep -qw "$name"; then
    echo "  keep framework: $name"
  else
    echo "  rm framework: $name"
    rm -rf "$d"
  fi
done < <(find "$APP_DIR" -name 'Qt*.framework' -type d)

# 5) Keep only the plugin families a widgets app needs at runtime.
KEEP_PLUGINS="platforms imageformats styles iconengines tls"
while IFS= read -r plugroot; do
  for d in "$plugroot"/*; do
    [ -d "$d" ] || continue
    bn=$(basename "$d")
    if echo " $KEEP_PLUGINS " | grep -qw "$bn"; then
      echo "  keep plugin: $bn"
    else
      echo "  rm plugin: $bn"
      rm -rf "$d"
    fi
  done
done < <(find "$APP_DIR" -type d -name plugins)

echo "== SIZE AFTER =="
du -sh "$APP_DIR"
