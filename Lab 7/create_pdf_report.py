import os
import shutil
import fitz
from fpdf import FPDF
from fpdf.enums import XPos, YPos

class ModernLabReport(FPDF):
    def header(self):
        self.set_font('Helvetica', 'B', 8.5)
        self.set_text_color(110, 120, 135)
        self.cell(0, 6, 'SE Lab 7: Fuzzing for Input Validation Bugs | Recycling Rewards', 
                  new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='R')
        self.set_draw_color(210, 215, 225)
        self.line(12, 14, 198, 14)
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(140, 145, 155)
        self.cell(0, 6, f'Page {self.page_no()}', 
                  new_x=XPos.LMARGIN, new_y=YPos.TOP, align='C')

def build_pdf():
    pdf = ModernLabReport(orientation='P', unit='mm', format='A4')
    pdf.set_margins(12, 10, 12)
    pdf.set_auto_page_break(auto=False)

    # ================= PAGE 1 =================
    pdf.add_page()
    pdf.set_fill_color(28, 45, 78)
    pdf.rect(12, 16, 186, 18, 'F')
    pdf.set_xy(12, 18)
    pdf.set_font('Helvetica', 'B', 15)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(186, 7, 'LAB 7: FUZZING FOR INPUT VALIDATION BUGS', 
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.set_font('Helvetica', '', 9.5)
    pdf.set_text_color(215, 230, 255)
    pdf.cell(186, 5, 'Software Engineering Laboratory | Property-Based Fuzz Testing with Hypothesis', 
             new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='C')
    pdf.ln(3)

    # Metadata Box
    pdf.set_fill_color(246, 248, 252)
    pdf.set_draw_color(218, 224, 235)
    pdf.rect(12, pdf.get_y(), 186, 24, 'DF')
    pdf.set_xy(16, pdf.get_y() + 2)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.set_text_color(35, 45, 65)
    pdf.cell(38, 5, 'Course & Semester:', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(52, 5, 'Software Engineering (Sem 5)', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(30, 5, 'Assigned Repo:', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(60, 5, 'L6_L7_50_recycling_rewards', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(16)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(38, 5, 'Application Script:', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(52, 5, 'recycling_rewards.py / processor.py', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(30, 5, 'Fuzzing Library:', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', '', 9)
    pdf.cell(60, 5, 'Hypothesis 6.170.15 + Pytest 9.1.1', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_x(16)
    pdf.set_font('Helvetica', 'B', 9)
    pdf.cell(38, 5, 'GitHub Repository:', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(0, 102, 204)
    pdf.cell(142, 5, 'https://github.com/rajatkooge5-learn/L6_L7_50_recycling_rewards', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # Objective & Concepts Box
    pdf.set_fill_color(240, 246, 255)
    pdf.set_draw_color(180, 205, 240)
    pdf.rect(12, pdf.get_y(), 186, 26, 'DF')
    pdf.set_xy(16, pdf.get_y() + 1.5)
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(24, 43, 73)
    pdf.cell(0, 5, 'Objective & Learning Outcomes', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(40, 50, 65)
    pdf.set_x(16)
    pdf.multi_cell(178, 4.2, 
        '- Methodology: Understand dynamic fuzz testing to discover hidden edge-case crashes.\n'
        '- Hypothesis Fuzzing: Apply property-based testing with @given strategies (st.text() | st.none()).\n'
        '- Shrinking & Diagnosis: Detect, analyze, and diagnose edge cases (None, empty string, delimiters).\n'
        '- Defensive Hardening: Apply defensive programming to guarantee 0 crashes on malformed inputs.')
    pdf.ln(3)

    # Step 1
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(28, 45, 78)
    pdf.cell(0, 5.5, 'Step 1: Installing Dependencies', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 4.2, 
        'Dependencies were installed via pip: "pip install hypothesis" and "pip install pytest".\n'
        'Installed environment: Python 3.13.7, hypothesis 6.170.15, sortedcontainers 2.4.0, pytest 9.1.1.')
    pdf.ln(2)

    # Step 2
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(28, 45, 78)
    pdf.cell(0, 5.5, 'Step 2: Run the Buggy Application Script', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 4.2, 
        'Command: "python processor.py" (or "python recycling_rewards.py").\n'
        'Standard valid inputs execute as expected, but the script completely lacks input validation, crashing instantly on malformed input.')
    pdf.ln(2)

    ss2 = 'C:/Users/rajat/OneDrive/sem 5/SE/Lab 7/Lab 7/Step2_Buggy_Application_Output.png'
    if os.path.exists(ss2):
        pdf.image(ss2, x=15, y=pdf.get_y(), w=180)

    # ================= PAGE 2 =================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(28, 45, 78)
    pdf.cell(0, 5.5, 'Step 3: Complete Test Suite using Hypothesis Fuzzing', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 3.8, 
        'Property-based test functions were implemented in "test_processor.py" and "test_recycling_rewards.py". '
        'Instead of asserting fixed outputs, the test verifies an invariant property: functions must never crash '
        'when given arbitrary text or None (st.text() | st.none()).')
    pdf.ln(1)

    # Code Box for Step 3
    box_y = pdf.get_y()
    code_text = (
        "from hypothesis import given, strategies as st\n"
        "from processor import parse_collection, weight_average, net_points\n\n"
        "@given(st.text() | st.none())\n"
        "def test_parse_collection_no_crash(s):\n"
        "    try: parse_collection(s)\n"
        "    except Exception as e: assert False, f'parse_collection crashed with: {e}'\n\n"
        "@given(st.text() | st.none())\n"
        "def test_weight_average_no_crash(s):\n"
        "    try: weight_average(s)\n"
        "    except Exception as e: assert False, f'weight_average crashed with: {e}'\n\n"
        "@given(st.text() | st.none())\n"
        "def test_net_points_no_crash(s):\n"
        "    try: net_points(s)\n"
        "    except Exception as e: assert False, f'net_points crashed with: {e}'"
    )
    box_height = 54
    pdf.set_fill_color(245, 247, 250)
    pdf.set_draw_color(210, 218, 230)
    pdf.rect(12, box_y, 186, box_height, 'DF')
    pdf.set_xy(15, box_y + 1.5)
    pdf.set_font('Courier', '', 7)
    pdf.set_text_color(20, 30, 45)
    pdf.multi_cell(180, 2.7, code_text)
    
    # Position Step 4 cleanly below the box
    pdf.set_xy(12, box_y + box_height + 4)
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(28, 45, 78)
    pdf.cell(0, 5, 'Step 4: Run the Test Suite on Buggy Code (Catching Failures)', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 3.6, 
        'Command: "pytest test_processor.py --tb=short" (or "python -m pytest test_processor.py").\n'
        'Hypothesis immediately discovered counterexamples causing crashes in all 3 functions:\n'
        '- test_parse_collection_no_crash: Crashed on s=None (AttributeError), s="" (ValueError), s=":" (ValueError)\n'
        '- test_weight_average_no_crash: Crashed on s=None (AttributeError), s="" (ValueError)\n'
        '- test_net_points_no_crash: Crashed on s=None (AttributeError), s="" (ValueError), s="|" (ValueError)')
    pdf.ln(1)

    ss4 = 'C:/Users/rajat/OneDrive/sem 5/SE/Lab 7/Lab 7/Step4_Hypothesis_Test_Failures.png'
    if os.path.exists(ss4):
        pdf.image(ss4, x=15, y=pdf.get_y(), w=180, h=108)

    # ================= PAGE 3 =================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(28, 45, 78)
    pdf.cell(0, 5.5, 'Step 5: Fix the Buggy Application Python Script (Defensive Programming)', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 4.2, 
        'The functions in "processor.py" and "recycling_rewards.py" were hardened defensively:\n'
        '- parse_collection(text): Validates isinstance(text, str), verifies exactly 2 split parts, strips whitespaces, validates non-empty material name, safely parses float kg, guards against NaN/Inf/negative weights. Returns None on invalid input.\n'
        '- weight_average(weights_csv): Validates isinstance(weights_csv, str), filters empty tokens (handles "1,,3"), converts integers safely, prevents ZeroDivisionError when list is empty. Returns 0 on invalid input.\n'
        '- net_points(text): Validates isinstance(text, str), verifies 2 parts split by "|", parses points and penalty to float safely, checks for NaN/Inf, calculates max(points*2 - penalty, 0.0). Returns 0.0 on invalid input.')
    pdf.ln(1)

    ss5 = 'C:/Users/rajat/OneDrive/sem 5/SE/Lab 7/Lab 7/Step5_Fixed_Application_Output.png'
    if os.path.exists(ss5):
        pdf.image(ss5, x=15, y=pdf.get_y(), w=180, h=75)
    pdf.set_y(pdf.get_y() + 77)

    # Step 6
    pdf.set_font('Helvetica', 'B', 10.5)
    pdf.set_text_color(28, 45, 78)
    pdf.cell(0, 5.5, 'Step 6: Re-Run the Test Suite on Fixed Code (100% Passing)', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8.5)
    pdf.set_text_color(50, 50, 50)
    pdf.multi_cell(0, 4.2, 
        'Command: "pytest test_processor.py" and "pytest test_recycling_rewards.py".\n'
        'All property-based fuzz tests passed successfully with 0 crashes across hundreds of randomized Unicode inputs.')
    pdf.ln(1)

    ss6 = 'C:/Users/rajat/OneDrive/sem 5/SE/Lab 7/Lab 7/Step6_Hypothesis_Tests_Passing.png'
    if os.path.exists(ss6):
        pdf.image(ss6, x=15, y=pdf.get_y(), w=180, h=80)

    # ================= PAGE 4 =================
    pdf.add_page()
    pdf.set_font('Helvetica', 'B', 12)
    pdf.set_text_color(28, 45, 78)
    pdf.cell(0, 6, 'Comprehensive Bug Analysis & Fixes Summary', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    table_data = [
        ["Function", "Root Cause / Bug", "Failing Input (Shrunk)", "Defensive Fix Applied"],
        ["parse_collection", 
         "1. NoneType split\n2. Missing ':' delimiter\n3. Non-numeric float", 
         "s = None\ns = ''\ns = ':'", 
         "isinstance check; 2-parts check; safe float conversion; return None on failure."],
        ["weight_average", 
         "1. NoneType split\n2. Empty token in CSV\n3. ZeroDivisionError", 
         "s = None\ns = ''\ns = '1,,3'", 
         "Filter empty items; safe integer parsing; len > 0 guard; return 0 on failure."],
        ["net_points", 
         "1. NoneType split\n2. Missing '|' delimiter\n3. Non-numeric points/penalty", 
         "s = None\ns = ''\ns = '|'", 
         "isinstance check; 2-parts check; safe float cast; return 0.0 on failure."]
    ]

    with pdf.table(col_widths=(35, 45, 38, 68), text_align=("LEFT", "LEFT", "LEFT", "LEFT")) as table:
        for i, row in enumerate(table_data):
            row_cells = table.row()
            for cell_text in row:
                if i == 0:
                    pdf.set_font('Helvetica', 'B', 9)
                else:
                    pdf.set_font('Helvetica', '', 8.5)
                row_cells.cell(cell_text)

    pdf.ln(4)

    # Comparison Callout Box
    pdf.set_fill_color(254, 250, 240)
    pdf.set_draw_color(240, 200, 120)
    box_y2 = pdf.get_y()
    pdf.rect(12, box_y2, 186, 25, 'DF')
    pdf.set_xy(16, box_y2 + 1.5)
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(150, 80, 0)
    pdf.cell(0, 5, 'Why Fuzz Testing Outperforms Traditional Unit Testing', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(70, 60, 40)
    pdf.set_x(16)
    pdf.multi_cell(178, 4, 
        '- Traditional Unit Tests only test expected scenarios and happy paths thought of by developers.\n'
        '- Hypothesis Fuzzing automatically generates thousands of malformed, unexpected, boundary, and edge-case inputs.\n'
        '- Automated Shrinking minimizes failing inputs to their simplest reproducible form (e.g., None, empty string, single delimiter).\n'
        '- Guarantees high software robustness, security against injection/DoS, and defensive reliability.')
    pdf.set_y(box_y2 + 28)

    # Deliverables Verification Box
    pdf.set_fill_color(240, 252, 244)
    pdf.set_draw_color(170, 230, 190)
    box_y3 = pdf.get_y()
    pdf.rect(12, box_y3, 186, 27, 'DF')
    pdf.set_xy(16, box_y3 + 1.5)
    pdf.set_font('Helvetica', 'B', 9.5)
    pdf.set_text_color(20, 110, 50)
    pdf.cell(0, 5, 'Submission Deliverables Checklist (Completed)', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 8)
    pdf.set_text_color(30, 60, 40)
    pdf.set_x(16)
    pdf.multi_cell(178, 4.2, 
        '[X] Deliverable 1: PDF Document with All Screenshots (Lab7_Fuzzing_Report.pdf)\n'
        '[X] Deliverable 2: Fixed application script (processor.py & recycling_rewards.py)\n'
        '[X] Deliverable 3: Updated test script (test_processor.py & test_recycling_rewards.py)\n'
        '[X] GitHub Repository Pushed: https://github.com/rajatkooge5-learn/L6_L7_50_recycling_rewards')

    out1 = 'C:/Users/rajat/OneDrive/sem 5/SE/Lab 7/Lab 7/Lab7_Fuzzing_Report.pdf'
    out2 = 'C:/Users/rajat/OneDrive/sem 5/SE/Lab 7/Lab7_Fuzzing_Report.pdf'
    pdf.output(out1)
    shutil.copyfile(out1, out2)
    print(f"Generated clean report at:\n  {out1}\n  {out2}")

if __name__ == '__main__':
    build_pdf()
