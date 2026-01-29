try:
    import pdfminer
    print("pdfminer installed")
except ImportError:
    print("pdfminer NOT installed")

try:
    import docx
    print("docx installed")
except ImportError:
    print("docx NOT installed")
