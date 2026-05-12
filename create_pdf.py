from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
import re

# 한글 폰트 등록 (맑은 고딕)
try:
    malgun_regular = "C:\\Windows\\Fonts\\malgun.ttf"
    malgun_bold = "C:\\Windows\\Fonts\\malgunbd.ttf"
    pdfmetrics.registerFont(TTFont('MalgunGothic', malgun_regular))
    pdfmetrics.registerFont(TTFont('MalgunGothic-Bold', malgun_bold))
    FONT_NAME = 'MalgunGothic'
    FONT_NAME_BOLD = 'MalgunGothic-Bold'
except Exception as e:
    print(f"⚠️ 한글 폰트 등록 오류: {e}")
    FONT_NAME = 'Helvetica'
    FONT_NAME_BOLD = 'Helvetica-Bold'

# 마크다운 파일 읽기
md_path = Path('ch05/SD_분석_디지털전환사례.md')
with open(md_path, 'r', encoding='utf-8') as f:
    md_content = f.read()

# PDF 생성
pdf_path = 'ch05/SD_분석_디지털전환사례.pdf'
doc = SimpleDocTemplate(pdf_path, pagesize=A4, topMargin=1.5*cm, bottomMargin=1.5*cm)

styles = getSampleStyleSheet()

# 한글 스타일 정의
title_style = ParagraphStyle(
    'CustomTitle',
    parent=styles['Heading1'],
    fontName=FONT_NAME_BOLD,
    fontSize=18,
    textColor=colors.HexColor('#000000'),
    spaceAfter=12,
    spaceBefore=6,
    alignment=TA_LEFT,
)

heading2_style = ParagraphStyle(
    'CustomHeading2',
    parent=styles['Heading2'],
    fontName=FONT_NAME_BOLD,
    fontSize=14,
    textColor=colors.HexColor('#0066cc'),
    spaceAfter=10,
    spaceBefore=8,
    alignment=TA_LEFT,
)

heading3_style = ParagraphStyle(
    'CustomHeading3',
    parent=styles['Heading3'],
    fontName=FONT_NAME,
    fontSize=12,
    textColor=colors.HexColor('#0099ff'),
    spaceAfter=8,
    spaceBefore=6,
    alignment=TA_LEFT,
)

body_style = ParagraphStyle(
    'CustomBody',
    parent=styles['BodyText'],
    fontName=FONT_NAME,
    fontSize=10,
    alignment=TA_LEFT,
    spaceAfter=6,
)

table_style = ParagraphStyle(
    'TableText',
    parent=styles['BodyText'],
    fontName=FONT_NAME,
    fontSize=8,
    alignment=TA_LEFT,
)

# 컨텐츠 빌드
story = []

# 마크다운 파싱
lines = md_content.split('\n')
i = 0
while i < len(lines):
    line = lines[i]
    
    # 제목
    if line.startswith('# '):
        title_text = line[2:].strip()
        story.append(Paragraph(title_text, title_style))
        story.append(Spacer(1, 0.1*inch))
    
    elif line.startswith('## '):
        heading_text = line[3:].strip()
        story.append(Paragraph(heading_text, heading2_style))
        story.append(Spacer(1, 0.05*inch))
    
    elif line.startswith('### '):
        heading_text = line[4:].strip()
        story.append(Paragraph(heading_text, heading3_style))
        story.append(Spacer(1, 0.05*inch))
    
    elif line.startswith('#### '):
        heading_text = line[5:].strip()
        story.append(Paragraph('<b>' + heading_text + '</b>', body_style))
        story.append(Spacer(1, 0.03*inch))
    
    # 테이블 감지
    elif line.strip().startswith('|'):
        table_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip().startswith('|'):
            if not lines[i].strip().startswith('|-') and not lines[i].strip().startswith('|---'):
                table_lines.append(lines[i])
            i += 1
        
        # 테이블 파싱
        if len(table_lines) >= 2:
            header = [cell.strip() for cell in table_lines[0].split('|')[1:-1]]
            rows = []
            for line_text in table_lines[1:]:
                if line_text.strip() and not '---' in line_text:
                    cells = [cell.strip() for cell in line_text.split('|')[1:-1]]
                    if len(cells) == len(header):
                        rows.append(cells)
            
            if rows:
                # 테이블 생성 - 셀을 Paragraph로 래핑하여 한글 폰트 적용
                table_header = [Paragraph(h, table_style) for h in header]
                table_data = [table_header]
                for row in rows:
                    wrapped_row = [Paragraph(cell, table_style) for cell in row]
                    table_data.append(wrapped_row)
                
                table = Table(table_data, colWidths=[1.5*cm] * len(header))
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f5f5f5')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), FONT_NAME_BOLD),
                    ('FONTNAME', (0, 1), (-1, -1), FONT_NAME),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('TOPPADDING', (0, 0), (-1, -1), 6),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#ddd')),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f9f9f9')]),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ]))
                story.append(table)
                story.append(Spacer(1, 0.1*inch))
        continue
    
    # 코드블록 스킵
    elif line.strip().startswith('```'):
        i += 1
        while i < len(lines) and not lines[i].strip().endswith('```'):
            i += 1
    
    # 구분선
    elif line.strip() == '---':
        story.append(Spacer(1, 0.1*inch))
    
    # 목록 항목
    elif line.strip().startswith('- '):
        list_text = line[2:].strip()
        story.append(Paragraph('• ' + list_text, body_style))
    
    # 일반 텍스트 (공백 아님)
    elif line.strip():
        # 마크다운 포매팅 간단히 처리
        text_formatted = line.strip()
        # 굵게: **text** → <b>text</b>
        text_formatted = re.sub(r'\*\*([^\*]+)\*\*', r'<b>\1</b>', text_formatted)
        story.append(Paragraph(text_formatted, body_style))
    
    i += 1

# PDF 생성
try:
    doc.build(story)
    print(f'✅ PDF 생성 완료')
    print(f'파일: {pdf_path}')
    print(f'크기: {Path(pdf_path).stat().st_size / 1024:.1f} KB')
except Exception as e:
    print(f'❌ 오류: {e}')
