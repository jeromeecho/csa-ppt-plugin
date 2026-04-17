#!/bin/bash
# Hook: Enforce PPT slide HTML rules
# Triggered on Write/Edit of *.html files in slide directories
#
# Rules enforced:
# 1. No full-width dark background bars (background: #4472C4 or #2F5496 on full-width elements)
# 2. Body dimensions must match 960pt x 540pt (when targeting that PPTX size)
# 3. Title must not be centered in a colored background bar

FILE="$1"

# Only check slide HTML files (skip non-slide files)
if [[ ! "$FILE" =~ slide.*\.html$ ]] && [[ ! "$FILE" =~ /slide[0-9]*/.*\.html$ ]]; then
  exit 0
fi

# Skip if file doesn't exist
if [ ! -f "$FILE" ]; then
  exit 0
fi

ERRORS=""

# Rule 1: Check for full-width dark background bars
# Only flag when background:#4472C4 or #2F5496 appears with width:960pt (full-width)
# This allows small accent uses (dots, borders, text colors)
if grep -E 'width:\s*960pt' "$FILE" | grep -qiE 'background:\s*#(4472C4|2F5496)'; then
  ERRORS="${ERRORS}\n[VIOLATION] 禁止全幅深色横条: 发现 width:960pt 元素使用 background:#4472C4 或 #2F5496"
fi

# Also check CSS classes that combine full-width + dark background
# Pattern: a CSS rule with width:960pt AND background:#4472C4/#2F5496
python3 -c "
import re, sys
with open('$FILE', 'r') as f:
    content = f.read()

# Find CSS blocks with both width:960pt and background:#4472C4 or #2F5496
# Split by CSS rule boundaries
css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if css_match:
    css = css_match.group(1)
    # Split into rules
    rules = re.split(r'\}', css)
    for rule in rules:
        if re.search(r'width:\s*960pt', rule) and re.search(r'background:\s*#(4472C4|2F5496)', rule, re.I):
            name = re.search(r'([.#\w-]+)\s*\{', rule)
            cls = name.group(1) if name else 'unknown'
            print(f'FULLWIDTH_DARK:{cls}')
" 2>/dev/null | while read line; do
  cls=$(echo "$line" | cut -d: -f2)
  ERRORS="${ERRORS}\n[VIOLATION] 禁止全幅深色横条: CSS类 $cls 同时使用 width:960pt 和深色背景"
done

# Rule 2: Check body dimensions match 960x540 (when present)
if grep -q 'width:\s*960pt' "$FILE"; then
  if ! grep -q 'height:\s*540pt' "$FILE"; then
    ERRORS="${ERRORS}\n[VIOLATION] 尺寸不匹配: 发现 width:960pt 但缺少 height:540pt"
  fi
fi

# Rule 3: Detect title-bar class with full-width colored background in CSS
python3 -c "
import re
with open('$FILE', 'r') as f:
    content = f.read()
css_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if css_match:
    css = css_match.group(1)
    rules = re.split(r'\}', css)
    for rule in rules:
        if re.search(r'\.title[-_]?bar', rule, re.I):
            if re.search(r'background:\s*#(4472C4|2F5496|ED7D31)', rule, re.I):
                if re.search(r'width:\s*(960pt|100%)', rule):
                    print('TITLE_BAR_VIOLATION')
" 2>/dev/null | grep -q "TITLE_BAR_VIOLATION"
if [ $? -eq 0 ]; then
  ERRORS="${ERRORS}\n[VIOLATION] 禁止蓝色标题栏: title-bar 类使用全幅深色背景"
fi

if [ -n "$ERRORS" ]; then
  echo -e "=== PPT Slide HTML 规则检查 ===$ERRORS"
  echo ""
  echo "参考: CLAUDE.md §2 禁止使用的样式 + §7 高度填充规则"
  exit 1
fi

exit 0
