#!/bin/bash

# PDF Book Generator Script
# 生成完整的 PDF 書籍

set -e

# 進入 docs 目錄
cd "$(cd "$(dirname "$0")" && pwd)/../docs"

# 定義檔案順序
FILES=(
  "01_PROJECT_OVERVIEW.md"
  "02_SYSTEM_ARCHITECTURE.md"
  "03_FEATURE_MODULES.md"
  "04_DATABASE_SCHEMA.md"
  "05_INSTALLATION_SETUP.md"
  "06_DEVELOPMENT_WORKFLOW.md"
  "07_TESTING_GUIDE.md"
  "08_DEPLOYMENT_GUIDE.md"
  "09_USER_MANUAL_OVERVIEW.md"
  "10_USER_GUIDE_INSTRUCTOR.md"
  "11_USER_GUIDE_ADMIN.md"
  "12_QUICK_START_GUIDE.md"
  "13_API_REFERENCE.md"
  "14_FRONTEND_COMPONENTS.md"
  "15_TROUBLESHOOTING.md"
)

echo "📚 開始生成完整文檔 PDF..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 生成 PDF（使用 XeLaTeX 以支持中文）
pandoc \
  metadata.yaml \
  "${FILES[@]}" \
  -H <(cat << 'EOF'
\usepackage{fontspec}
% emoji 字體會由系統自動選擇適當的備選
EOF
) \
  --pdf-engine=xelatex \
  --from=markdown \
  --to=pdf \
  --toc \
  --toc-depth=3 \
  --number-sections \
  --top-level-division=chapter \
  --variable=fontsize:12pt \
  --variable=geometry:"margin=2.5cm" \
  --variable=linestretch:1.5 \
  --variable=colorlinks:true \
  --variable=linkcolor:blue \
  --variable=urlcolor:blue \
  --variable=mainfont:"Noto Sans" \
  --variable=sansfont:"Noto Sans" \
  --variable=monofont:"Noto Sans Mono" \
  --variable=CJKmainfont:"Noto Serif CJK TC" \
  --variable=toc-title:"目錄" \
  --variable=lang:"zh-TW" \
  -o complete_book.pdf

echo ""
echo "✅ PDF 生成完成！"
echo "📄 檔案位置: $(pwd)/complete_book.pdf"
echo "📊 檔案大小: $(du -h complete_book.pdf | cut -f1)"
echo ""
echo "🎉 現在你有一本完整的文檔書籍！"
