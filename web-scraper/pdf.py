import fitz  # PyMuPDF
import re

def clean_pdf_to_md(pdf_path, output_path):
    doc = fitz.open(pdf_path)
    md_content = "# DeKUT GOK Fee Structures 2025/2026\n\n"
    
    # We want to capture the unique parts of each page
    # and ignore the repeated payment instructions to save tokens.
    for page_num, page in enumerate(doc):
        text = page.get_text()
        
        # Extract the Programme Name (usually after 'Applicable to')
        prog_match = re.search(r"Applicable to (?:the following Programmes:|BACHELOR OF)(.*?)The following table", text, re.DOTALL | re.IGNORECASE)
        
        # Extract the Fee amounts
        fee_match = re.search(r"TOTAL PAYABLE.*?([\d,]+\.?\d*).*?([\d,]+\.?\d*).*?([\d,]+\.?\d*)", text, re.DOTALL)
        
        if prog_match and fee_match:
            programs = prog_match.group(1).strip().replace('\n', ' ')
            sem1, sem2, yearly = fee_match.groups()
            
            md_content += f"## {programs}\n"
            md_content += f"| Period | Amount (KES) |\n| :--- | :--- |\n"
            md_content += f"| Semester I | {sem1} |\n"
            md_content += f"| Semester II | {sem2} |\n"
            md_content += f"| **Total Yearly** | **{yearly}** |\n\n"
            md_content += "---\n\n"

    with open(output_path, "w") as f:
        f.write(md_content)
    print(f"✅ Created clean Markdown at: {output_path}")

clean_pdf_to_md("dedan kimathi db/gok.pdf", "dedan kimathi db/gok_fees_cleaned.md")