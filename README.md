# 📄 PDF Auto-Splitter (Python CLI)

가로로 스캔된 2페이지 분량의 PDF를 **낱개 페이지(1페이지씩)**로 자동 분할해 주는 파이썬 도구입니다. 외부 웹사이트 업로드 없이 로컬 환경에서 안전하게 처리할 수 있습니다.

## 🚀 주요 기능

* **지능형 분할**: 페이지의 `MediaBox` 좌표를 계산하여 정중앙을 기준으로 좌/우 분할
* **일괄 처리 지원**: 단일 파일뿐만 아니라 폴더 내 모든 PDF 처리 가능 (확장 가능)
* **데이터 보안**: 외부 서버 전송 없이 로컬 라이브러리(`PyPDF2`)만 사용

---

## 🛠 설치 및 준비

### 1. 필수 조건

* **Python 3.6+** 가 설치되어 있어야 합니다.
* **Gemini CLI** 또는 터미널 환경에서 작업합니다.

### 2. 라이브러리 설치

터미널에 아래 명령어를 입력하여 필요한 패키지를 설치하세요.

```bash
pip install PyPDF2

```

---

## 💻 사용 방법

### 1. 스크립트 파일 작성

`split_pdf.py` 파일을 생성하고 아래 코드를 저장합니다.

```python
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

```

### 2. CLI에서 실행

터미널에서 변환하고자 하는 PDF 파일명을 인자로 넣어 실행합니다.

```bash
python split_pdf.py input_file.pdf

```

---

## 📂 프로젝트 구조

```text
.
├── split_pdf.py    # 실행 스크립트
├── input_file.pdf  # 원본 파일 (가로 2면)
└── README.md       # 프로젝트 설명서

```

---

## ⚠️ 참고 사항

* **여백 조절**: 스캔 상태에 따라 중앙선이 맞지 않을 경우, 코드 내 `middle_x` 값에 오프셋(예: `+10` 또는 `-10`)을 더해 조정할 수 있습니다.
* **암호화된 PDF**: 암호가 걸린 파일은 먼저 암호를 해제한 후 작업해야 합니다.

---

**Would you like me to add a batch processing feature that automatically scans an entire folder and splits all PDF files at once?**