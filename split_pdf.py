import PyPDF2
import os
import sys
import copy

def split_pdf(input_path, output_dir):
    """
    가로로 긴 PDF 페이지를 절반으로 나누어 두 개의 세로 페이지로 분할합니다.
    """
    file_name = os.path.basename(input_path)
    output_path = os.path.join(output_dir, file_name)
    
    try:
        with open(input_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            writer = PyPDF2.PdfWriter()

            for i, page in enumerate(reader.pages):
                mb = page.mediabox
                width = mb.upper_right[0] - mb.lower_left[0]
                height = mb.upper_right[1] - mb.lower_left[1]

                # 가로가 세로보다 길 경우에만 분할 (2면 합침 감지)
                if width > height:
                    # 1. 왼쪽 페이지 생성 및 독립적 복제
                    page_left = copy.copy(page)
                    page_left.mediabox = copy.copy(mb)
                    middle_x = (mb.lower_left[0] + mb.upper_right[0]) / 2

                    # 왼쪽 절반으로 영역 제한 (MediaBox & CropBox)
                    page_left.mediabox.upper_right = (middle_x, mb.upper_right[1])
                    page_left.cropbox = copy.copy(page_left.mediabox)
                    writer.add_page(page_left)

                    # 2. 오른쪽 페이지 생성 및 독립적 복제
                    page_right = copy.copy(page)
                    page_right.mediabox = copy.copy(mb)
                    
                    # 오른쪽 절반으로 영역 제한 (MediaBox & CropBox)
                    page_right.mediabox.lower_left = (middle_x, mb.lower_left[1])
                    page_right.cropbox = copy.copy(page_right.mediabox)
                    writer.add_page(page_right)
                else:
                    # 가로보다 세로가 길거나 같으면 그대로 유지
                    writer.add_page(page)

            with open(output_path, "wb") as out_f:
                writer.write(out_f)
        
        print(f"✅ 분할 완료: {output_path}")
    except Exception as e:
        print(f"❌ 오류 발생 ({file_name}): {e}")

def process_all_pdfs():
    source_dir = "PDF"
    target_base_dir = "Splitter"

    if not os.path.exists(source_dir):
        print(f"❌ '{source_dir}' 디렉토리가 존재하지 않습니다.")
        return

    if not os.path.exists(target_base_dir):
        os.makedirs(target_base_dir)

    pdf_files = [f for f in os.listdir(source_dir) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"ℹ️ '{source_dir}' 폴더에 PDF 파일이 없습니다.")
        return

    for pdf_file in pdf_files:
        dir_name = os.path.splitext(pdf_file)[0]
        target_dir = os.path.join(target_base_dir, dir_name)

        if os.path.exists(target_dir):
            print(f"⏭️  건너뜀 (이미 존재함): {dir_name}")
            continue

        os.makedirs(target_dir)
        input_path = os.path.join(source_dir, pdf_file)
        split_pdf(input_path, target_dir)

if __name__ == "__main__":
    process_all_pdfs()
