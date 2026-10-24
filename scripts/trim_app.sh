#!/bin/bash
# Aggressively shrink a py2app PySide6 bundle.
#
# py2app's PySide6 recipe copies the ENTIRE PySide6 wheel: every Qt framework,
# the whole Qt/qml tree, plugins, headers, translations. For a plain
# QtWidgets app we only need QtCore/QtGui/QtWidgets/QtNetwork/QtSvg (+ their
# transitive deps). Everything else is dead weight.
#
# Strategy:
#   1. Delete the Qt/qml tree and unused PySide6 Qt*.so modules up front, so
#      the otool reference scan (step 3) no longer "sees" frameworks that were
#      only referenced by QML/Quick/etc.
#   2. Delete unreferenced Qt*.framework dirs (otool -L based — safe).
#   3. Delete unused Qt plugin families and translation/header bloat.
set -u

APP_DIR=$(ls -d dist/*.app 2>/dev/null | head -n1)
if [ -z "$APP_DIR" ]; then
  echo "ERROR: no built .app found in dist/" >&2
  exit 1
fi

PS="$APP_DIR/Contents/Resources/lib/python3.11/PySide6"
SH="$APP_DIR/Contents/Resources/lib/python3.11/shiboken6"

echo "== SIZE BEFORE =="
du -sh "$APP_DIR"

# 1) We are a QtWidgets app, not QML -> drop the entire QML tree (huge).
rm -rf "$PS/Qt/qml"
# 2) Drop dev-only headers.
rm -rf "$PS/include" "$SH/include"
# 3) Keep only the PySide6 modules a widgets app imports; delete the rest
#    (this is what stops otool from "seeing" QtQuick/QtQml/Qt3D references).
if [ -d "$PS" ]; then
  for m in "$PS"/Qt*.so; do
    [ -e "$m" ] || continue
    case "$(basename "$m")" in
      QtCore.so|QtGui.so|QtWidgets.so|QtNetwork.so|QtSvg.so) ;;
      *) rm -f "$m" ;;
    esac
  done
fi

# 4) Delete Qt frameworks nothing references (otool -L based).
REFS=$(mktemp)
while IFS= read -r f; do
  otool -L "$f" 2>/dev/null
done < <(find "$APP_DIR" \( -name "*.so" -o -name "*.dylib" -o -name "Python" \) -type f) \
  | grep -oE 'Qt[A-Za-z0-9]+\.framework' \
  | sort -u > "$REFS"

echo "== Referenced Qt frameworks (KEPT) =="
cat "$REFS"

while IFS= read -r d; do
  [ -d "$d" ] || continue
  name=$(basename "$d" .framework)
  if ! grep -qx "$name.framework" "$REFS"; then
    echo "  rm framework: $name"
    rm -rf "$d"
  fi
done < <(find "$APP_DIR" -name 'Qt*.framework' -type d)

# 5) Keep only the plugin families a widgets app needs at runtime.
KEEP="platforms imageformats styles iconengines tls"
while IFS= read -r plugroot; do
  for d in "$plugroot"/*; do
    [ -d "$d" ] || continue
    bn=$(basename "$d")
    if ! echo "$KEEP" | grep -qw "$bn"; then
      echo "  rm plugin: $bn"
      rm -rf "$d"
    fi
  done
done < <(find "$APP_DIR" -type d -name plugins)

# 6) Qt translations are not needed for our own (i18n-driven) UI.
rm -rf "$PS/Qt/translations"
rm -rf "$PS/Qt/resources" 2>/dev/null || true

rm -f "$REFS"

echo "== SIZE AFTER =="
du -sh "$APP_DIR"
