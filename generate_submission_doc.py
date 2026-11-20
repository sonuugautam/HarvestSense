"""
Generates the official 1-page CSE 473 Project Submission Sheet for Sonu Kumar
matching the exact formatting from the uploaded template sample.
"""

import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_submission_sheet():
    doc = Document()
    
    # 1-inch standard margins
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    def add_centered_para(text, font_size=18, is_bold=False, space_before=10, space_after=10, color=RGBColor(0, 0, 0), is_link=False):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        run = p.add_run(text)
        run.font.name = 'Calibri'
        run.font.size = Pt(font_size)
        run.bold = is_bold
        run.font.color.rgb = color
        if is_link:
            run.underline = True
        return p

    # 1. Project Title
    add_centered_para("HARVESTSENSE PROJECT", font_size=24, is_bold=True, space_before=20, space_after=18)

    # 2. Course Code
    add_centered_para("CSE 473", font_size=20, is_bold=False, space_before=10, space_after=18)

    # 3. Name
    add_centered_para("NAME – SONU KUMAR", font_size=20, is_bold=False, space_before=10, space_after=18)

    # 4. Reg No
    add_centered_para("REG NO – 12322453", font_size=20, is_bold=False, space_before=10, space_after=18)

    # 5. Roll No (leaving placeholder so student can write or edit)
    add_centered_para("ROLL NO – 38", font_size=20, is_bold=False, space_before=10, space_after=18)

    # 6. Section
    add_centered_para("SECTION – K23AP", font_size=20, is_bold=False, space_before=10, space_after=18)

    # 7. Submitted to
    add_centered_para("SUBMITTED TO – MR RAVNEET SINGH", font_size=20, is_bold=False, space_before=10, space_after=18)

    # 8. GitHub link header
    add_centered_para("GITHUB PROJECT LINK –", font_size=20, is_bold=False, space_before=10, space_after=4)

    # 9. GitHub actual URL
    add_centered_para("https://github.com/sonuugautam/HarvestSense", font_size=16, is_bold=False, space_before=2, space_after=22, color=RGBColor(37, 99, 235), is_link=True)

    # 10. Project ID Proof Title
    add_centered_para("PROJECT ID PROOF –", font_size=20, is_bold=False, space_before=12, space_after=14)

    # 11. Image of the table row
    image_path = os.path.abspath("project_id_proof.png")
    if os.path.exists(image_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(10)
        run_img = p_img.add_run()
        run_img.add_picture(image_path, width=Inches(6.5))

    docx_output = "HarvestSense_CSE473_Project_Submission.docx"
    doc.save(docx_output)
    print(f"SUCCESS: Saved {docx_output}")
    return docx_output

if __name__ == "__main__":
    create_submission_sheet()
