#!/bin/bash

# PDF Book Generator Script
# 生成完整的 PDF 書籍

set -e

# 進入 docs 目錄
cd "$(cd "$(dirname "$0")" && pwd)/../docs"

# 定義檔案順序
FILES=(
  "01_RESEARCH_MOTIVATION.md"
  "02_RESEARCH_METHODS.md"
  "03_RESULTS.md"
  "04_UNEXPECTED_OBSERVATIONS.md"
  "05_CONCLUSIONS_AND_RECOMMENDATIONS.md"
)

echo "📚 開始生成完整文檔 PDF..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 生成 PDF（使用 XeLaTeX 以支持中文）
pandoc \
  --metadata-file=metadata.yaml \
  "${FILES[@]}" \
  -H <(cat << 'EOF'
\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{caption}
\usepackage{float}
% emoji 字體會由系統自動選擇適當的備選
\setmainfont{Noto Sans}
\setsansfont{Noto Sans}
\setmonofont{Noto Sans Mono}
\setCJKmainfont{Noto Serif CJK TC}
\setCJKsansfont{Noto Sans CJK TC}
\setCJKmonofont{Noto Sans CJK TC}
\renewcommand{\figurename}{圖}
\renewcommand{\tablename}{表}
\renewcommand{\contentsname}{目錄}
\captionsetup[figure]{name=圖}
\captionsetup[table]{name=表}
\floatplacement{figure}{H}
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
  --variable=documentclass:"report" \
  --variable=classoption:"openany" \
  --variable=toc-title:"目錄" \
  --variable=lang:"zh-TW" \
  -o complete_book.pdf

echo ""
echo "✅ PDF 生成完成！"
echo "📄 檔案位置: $(pwd)/complete_book.pdf"
echo "📊 檔案大小: $(du -h complete_book.pdf | cut -f1)"
echo ""
echo "🎉 現在你有一本完整的文檔書籍！"
