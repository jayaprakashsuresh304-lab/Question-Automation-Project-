#!/usr/bin/env python3
from docx import Document
from pathlib import Path

# Load template
orig = Document(r'C:\Users\PRAJEEN\Downloads\QP Template.docx')

# Save without any modifications
test_path = Path(r'C:\Users\PRAJEEN\AppData\Local\Temp\test_preserve.docx')
orig.save(str(test_path))

print(f"✓ Template saved to: {test_path}")
print(f"✓ Original size: check source file")
print(f"✓ Compare the test file with original to see if structure is preserved")
