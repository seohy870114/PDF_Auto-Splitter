import PyPDF2
import sys
import os

def split_pdf(input_path):
    output_path = f"split_{input_path}"
    
    with open(input_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        writer = PyPDF2.PdfWriter()

        for page in reader.pages:
            # 좌측 페이지 (Left Side)
            page_left = writer.add_page(page)
            lower_left = page_left.mediabox.lower_left
            upper_right = page_left.mediabox.upper_right
            middle_x = (lower_left[0] + upper_right[0]) / 2
            page_left.mediabox.upper_right = (middle_x, upper_right[1])

            # 우측 페이지 (Right Side)
            page_right = writer.add_page(page)
            page_right.mediabox.lower_left = (middle_x, lower_left[1])

        with open(output_path, "wb") as out_f:
            writer.write(out_f)
    
    print(f"✅ 완료: {output_path} 파일이 생성되었습니다.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python split_pdf.py <filename.pdf>")
    else:
        split_pdf(sys.argv[1])
