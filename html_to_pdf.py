from html2image import Html2Image
from PIL import Image
from fpdf import FPDF
import os
from pathlib import Path
import tempfile

# HTML 파일 경로
html_file = Path('exam/exam_q1_planning_process.html')
output_pdf = Path('exam/exam_q1_planning_process.pdf')

try:
    # 임시 디렉토리에 이미지 저장
    with tempfile.TemporaryDirectory() as tmpdir:
        # html2image를 사용하여 HTML을 이미지로 변환
        print("🔄 HTML을 이미지로 변환 중...")
        
        hti = Html2Image()
        # 페이지 크기를 A4로 설정
        images = hti.screenshot(url=f'file:///{html_file.absolute().as_posix()}', 
                               output_path=tmpdir,
                               css_string='body { margin: 0; padding: 10px; }')
    
    print(f"✅ {len(images)} 페이지 이미지 생성됨")
    
    # 이미지를 PDF로 변환
    print("🔄 이미지를 PDF로 변환 중...")
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    
    for img_path in sorted(images):
        # 이미지를 JPEG로 변환 (PDF 호환성)
        img = Image.open(img_path)
        
        # 이미지를 A4 사이즈에 맞게 조정
        a4_width = 210
        a4_height = 297
        
        # 이미지 비율 유지하며 리사이즈
        ratio = min(a4_width / img.width, a4_height / img.height)
        new_width = img.width * ratio
        new_height = img.height * ratio
        
        img_resized = img.resize((int(new_width), int(new_height)), Image.Resampling.LANCZOS)
        
        # 임시 저장
        temp_path = 'temp_img.jpg'
        img_resized.save(temp_path, 'JPEG', quality=95)
        
        # PDF에 추가
        pdf.add_page()
        pdf.image(temp_path, x=0, y=0, w=a4_width)
        
        # 임시 파일 삭제
        os.remove(temp_path)
    
    # PDF 저장
    pdf.output(str(output_pdf))
    print(f"✅ PDF 변환 완료: {output_pdf}")
    
except Exception as e:
    print(f"❌ 오류 발생: {e}")
    import traceback
    traceback.print_exc()
