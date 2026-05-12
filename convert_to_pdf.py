import asyncio
from pyppeteer import launch
import os

async def convert_html_to_pdf():
    browser = await launch()
    page = await browser.newPage()
    
    # HTML 파일을 PDF로 변환
    html_path = os.path.abspath('exam/exam_q1_planning_process.html')
    pdf_path = os.path.abspath('exam/exam_q1_planning_process.pdf')
    
    await page.goto(f'file:///{html_path}', {'waitUntil': 'networkidle2'})
    await page.pdf({'path': pdf_path, 'format': 'A4', 'margin': {'top': '1cm', 'bottom': '1cm', 'left': '1cm', 'right': '1cm'}})
    
    await browser.close()
    print(f'✅ PDF 변환 완료: exam/exam_q1_planning_process.pdf')

asyncio.run(convert_html_to_pdf())
