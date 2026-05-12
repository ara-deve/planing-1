#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image as RLImage
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import html

# 한글 폰트 등록
try:
    malgun_regular = "C:\\Windows\\Fonts\\malgun.ttf"
    malgun_bold = "C:\\Windows\\Fonts\\malgunbd.ttf"
    pdfmetrics.registerFont(TTFont('MalgunGothic', malgun_regular))
    pdfmetrics.registerFont(TTFont('MalgunGothic-Bold', malgun_bold))
    FONT = 'MalgunGothic'
    FONT_BOLD = 'MalgunGothic-Bold'
except:
    FONT = 'Helvetica'
    FONT_BOLD = 'Helvetica-Bold'

# Notebook 파일 로드
nb_path = Path('exam/exam_q1_planning_process.ipynb')
with open(nb_path, 'r', encoding='utf-8') as f:
    notebook = json.load(f)

# PDF 생성 설정
pdf_path = 'exam/exam_q1_planning_process.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm)

styles = getSampleStyleSheet()

# 한글 스타일 정의
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontName=FONT_BOLD,
    fontSize=16,
    textColor=colors.black,
    spaceAfter=12,
    spaceBefore=0,
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontName=FONT_BOLD,
    fontSize=13,
    textColor=colors.black,
    spaceAfter=10,
)

heading3_style = ParagraphStyle(
    'CustomHeading3',
    parent=styles['Heading3'],
    fontName=FONT_BOLD,
    fontSize=11,
    textColor=colors.black,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontName=FONT,
    fontSize=10,
    textColor=colors.black,
    spaceAfter=8,
)

# 문서에 추가할 요소 리스트
story = []

# Notebook 셀 처리
for cell in notebook['cells']:
    cell_type = cell.get('cell_type', '')
    source = ''.join(cell.get('source', []))
    
    if not source.strip():
        continue
    
    if cell_type == 'markdown':
        # 마크다운 처리
        lines = source.split('\n')
        for line in lines:
            if not line.strip():
                story.append(Spacer(1, 0.3*cm))
            elif line.startswith('# '):
                text = line[2:].strip()
                try:
                    story.append(Paragraph(text, title_style))
                except:
                    story.append(Paragraph('', title_style))
            elif line.startswith('## '):
                text = line[3:].strip()
                try:
                    story.append(Paragraph(text, heading2_style))
                except:
                    story.append(Paragraph('', heading2_style))
            elif line.startswith('### '):
                text = line[4:].strip()
                try:
                    story.append(Paragraph(text, heading3_style))
                except:
                    story.append(Paragraph('', heading3_style))
            elif line.startswith('---'):
                story.append(Spacer(1, 0.5*cm))
            elif line.strip().startswith('|'):
                # 표 처리 (간단히)
                story.append(Spacer(1, 0.2*cm))
            elif line.startswith('- '):
                text = line[2:].strip()
                try:
                    story.append(Paragraph('• ' + text, body_style))
                except:
                    pass
            else:
                if line.strip():
                    try:
                        # HTML 특수 문자 처리
                        clean_text = html.escape(line.strip())[:500]  # 길이 제한
                        story.append(Paragraph(clean_text, body_style))
                    except:
                        pass
    
    elif cell_type == 'code':
        # 코드 셀 - 실행 결과만 포함
        outputs = cell.get('outputs', [])
        for output in outputs:
            if output.get('output_type') == 'stream':
                text = ''.join(output.get('text', []))
                if text.strip():
                    try:
                        code_style = ParagraphStyle(
                            'Code',
                            fontName='Courier',
                            fontSize=8,
                            textColor=colors.black,
                        )
                        story.append(Paragraph('<b>실행 결과:</b>', body_style))
                        for line in text.split('\n')[:10]:  # 처음 10줄만
                            if line.strip():
                                story.append(Paragraph(line[:100], code_style))
                    except:
                        pass

# 페이지 구분
if len(story) > 100:
    # 너무 길면 중간에 페이지 구분
    story.insert(len(story)//2, PageBreak())

# PDF 생성
try:
    doc.build(story)
    print(f"✅ PDF 생성 완료: {pdf_path}")
except Exception as e:
    print(f"❌ PDF 생성 오류: {e}")
