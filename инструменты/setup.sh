#!/bin/bash
# Окружение для правок записок в облачной сессии (Ubuntu). Идемпотентно.
set -e
pip install -q matplotlib iapws python-docx pymupdf pillow 2>/dev/null || pip install matplotlib iapws python-docx pymupdf pillow
if ! fc-list | grep -q "NotoSerif-Bold"; then
  (apt-get install -y -q fonts-noto-core >/dev/null 2>&1 || (apt-get update -q >/dev/null && apt-get install -y -q fonts-noto-core >/dev/null))
fi
if ! fc-list | grep -qi osifont; then
  (apt-get install -y -q fonts-osifont >/dev/null 2>&1 || (apt-get update -q >/dev/null && apt-get install -y -q fonts-osifont >/dev/null))
fi
rm -rf ~/.cache/matplotlib
command -v soffice >/dev/null || echo "нет LibreOffice (soffice) – PDF не собрать"
command -v pdftotext >/dev/null || echo "нет poppler-utils (pdftotext, pdftoppm)"
echo "готово"
