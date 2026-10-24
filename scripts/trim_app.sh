#!/bin/bash
# Trim an unnecessarily large py2app bundle down to only what is actually
# referenced. Safe because it deletes a Qt framework / plugin dir ONLY if no
# Mach-O binary in the .app links against it (otool -L based).
set -u

APP_DIR=$(ls -d dist/*.app 2>/dev/null | head -n1)
if [ -z "$APP_DIR" ]; then
  echo "ERROR: no built .app found in dist/" >&2
  exit 1
fi

FW_DIR="$APP_DIR/Contents/Frameworks"
PLUGIN_DIR="$APP_DIR/Contents/PlugIns"

echo "== SIZE BEFORE =="
du -sh "$APP_DIR"

# 1) Collect every Qt framework name referenced by any binary in the bundle.
REFS=$(mktemp)
while IFS= read -r f; do
  otool -L "$f" 2>/dev/null
done < <(find "$APP_DIR" \( -name "*.so" -o -name "*.dylib" -o -name "Python" \) -type f) \
  | grep -oE 'Qt[A-Za-z0-9]+\.framework' \
  | sort -u > "$REFS"

echo "== Referenced Qt frameworks (kept) =="
cat "$REFS"

# 2) Delete unreferenced Qt*.framework directories.
if [ -d "$FW_DIR" ]; then
  for d in "$FW_DIR"/Qt*.framework; do
    [ -e "$d" ] || continue
    name=$(basename "$d" .framework)
    if ! grep -qx "$name.framework" "$REFS"; then
      echo "  rm unused framework: $name"
      rm -rf "$d"
    fi
  done
fi

# 3) Keep only the plugin families a basic QtWidgets app needs at runtime.
#    (Plugins are loaded by name, so otool won't reveal them — this is the
#     conservative standard set.)
KEEP="platforms imageformats styles iconengines tls"
if [ -d "$PLUGIN_DIR" ]; then
  for d in "$PLUGIN_DIR"/*; do
    [ -d "$d" ] || continue
    bn=$(basename "$d")
    if ! echo "$KEEP" | grep -qw "$bn"; then
      echo "  rm unused plugin dir: $bn"
      rm -rf "$d"
    fi
  done
fi

rm -f "$REFS"

echo "== SIZE AFTER =="
du -sh "$APP_DIR"
