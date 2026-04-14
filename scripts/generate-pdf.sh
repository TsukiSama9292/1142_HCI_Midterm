#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DOCS_DIR="$SCRIPT_DIR/../docs"
cd "$DOCS_DIR"

SYMLINK_CREATED=false
if [ ! -e "output" ]; then
  ln -s ../output output
  SYMLINK_CREATED=true
fi

echo "📚 開始在 docs 目錄中生成 PDF..."
quarto render --to pdf

if [ "$SYMLINK_CREATED" = true ]; then
  rm -f output
fi

OUTPUT="_book/docs.pdf"
if [ -f "$OUTPUT" ]; then
  echo "✅ PDF 生成完成：$(pwd)/$OUTPUT"
else
  echo "❌ PDF 生成失敗，未找到 $OUTPUT" >&2
  exit 1
fi
