#!/bin/sh
# Build the upload zip for xneelo: only the files the live site needs.
set -e
cd "$(dirname "$0")/.."
OUT="${1:-STAND_website_upload.zip}"
rm -f "$OUT"
zip -qr "$OUT" .htaccess *.html progress.txt give css js assets \
  -x "*.DS_Store" "assets/stand/hero-conference-original*"
echo "Wrote $OUT ($(du -h "$OUT" | cut -f1))"
