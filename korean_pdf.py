#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from fpdf import FPDF
import textwrap

# 한글을 지원하는 FPDF 클래스 확장
class KoreanPDF(FPDF):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 한글 폰트 추가 (DejaVuSans 대신 기본 폰트 사용)
        self.add_font("Arial", "", "C:\\Windows\\Fonts\\malgun.ttf")
        
    def multi_cell_ko(self, w, h, txt, border=0, align='L', fill=False):
        """한글 텍스트를 위한 multi_cell"""
        self.set_font("Arial", "", 11)
        self.multi_cell(w, h, txt, border=border, align=align, fill=fill)

# Notebook 파일 로드
nb_path = Path('exam/exam_q1_planning_process.ipynb')
with open(nb_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# PDF 생성
pdf = KoreanPDF('P', 'mm', 'A4')
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# 스타일 설정
title_size = 16
heading_size = 13
body_size = 10
line_height = 6

# 셀 처리
for cell in notebook['cells']:
    cell_type = cell.get('cell_type', '')
    source = ''.join(cell.get('source', []))
    
    if not source.strip():
        continue
    
    if cell_type == 'markdown':
        lines = source.split('\n')
        for line in lines:
            if not line.strip():
                pdf.ln(2)
            elif line.startswith('# '):
                pdf.set_font("Arial", "B", title_size)
                text = line[2:].strip()
                pdf.multi_cell(0, line_height, text)
                pdf.ln(2)
            elif line.startswith('## '):
                pdf.set_font("Arial", "B", heading_size)
                text = line[3:].strip()
                pdf.multi_cell(0, line_height, text)
                pdf.ln(1)
            elif line.startswith('### '):
                pdf.set_font("Arial", "B", heading_size - 2)
                text = line[4:].strip()
                pdf.multi_cell(0, line_height, text)
                pdf.ln(1)
            elif line.startswith('---'):
                pdf.ln(3)
            elif line.strip().startswith('|'):
                # 테이블 스킵 (복잡하므로)
                pdf.ln(1)
            elif line.startswith('- '):
                pdf.set_font("Arial", "", body_size)
                text = '• ' + line[2:].strip()
                pdf.multi_cell(0, line_height, text)
            elif line.startswith('**'):
                pdf.set_font("Arial", "B", body_size)
                text = line.replace('**', '')
                pdf.multi_cell(0, line_height, text)
            else:
                if line.strip():
                    pdf.set_font("Arial", "", body_size)
                    # 줄 길이 제한
                    wrapped_text = textwrap.fill(line.strip(), width=80)
                    pdf.multi_cell(0, line_height, wrapped_text)
    
    elif cell_type == 'code':
        # 실행 결과만 표시
        outputs = cell.get('outputs', [])
        for output in outputs:
            if output.get('output_type') == 'stream':
                text = ''.join(output.get('text', []))
                if text.strip():
                    pdf.set_font("Arial", "B", body_size - 1)
                    pdf.multi_cell(0, line_height - 2, "[실행 결과]")
                    pdf.set_font("Arial", "", body_size - 2)
                    for line in text.split('\n')[:15]:  # 처음 15줄만
                        if line.strip():
                            pdf.multi_cell(0, line_height - 2, line[:100])

# PDF 저장
pdf_path = 'exam/exam_q1_planning_process.pdf'
pdf.output(pdf_path)
print(f"✅ 한글 PDF 생성 완료: {pdf_path}")
