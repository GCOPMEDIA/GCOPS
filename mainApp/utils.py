from fpdf import FPDF
from .models import *
from django.db.models import Sum
from django.db.models import Window
from django.db.models.functions import Rank
from django.db.models import IntegerField
from django.db.models import F
from django.db.models.functions import Cast
from mainApp.models import Grade
def safe_text(text):
    text=str(text)
    return (text.replace("–", "-")
                .replace("’", "'")
                .replace("“", '"')
                .replace("”", '"')
                .replace("…", "..."))

from datetime import datetime

def shorten_level_name(level):
    level = level.strip().lower()

    if "kindergarten" in level or "kg" in level:
        number = ''.join(filter(str.isdigit, level))
        return f"KG{number}" if number else "KG"

    elif "nursery" in level or "n" in level:
        number = ''.join(filter(str.isdigit, level))
        return f"N{number}" if number else "N"

    elif "primary" in level:
        word_to_number = {
            "one": "1", "two": "2", "three": "3",
            "four": "4", "five": "5", "six": "6"
        }
        for word, num in word_to_number.items():
            if word in level:
                return f"B{num}"
        number = ''.join(filter(str.isdigit, level))
        return f"B{number}" if number else "B"

    return level.upper()

def number_to_ordinal(n):
    n = int(n)
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        last_digit = n % 10
        if last_digit == 1:
            suffix = 'st'
        elif last_digit == 2:
            suffix = 'nd'
        elif last_digit == 3:
            suffix = 'rd'
        else:
            suffix = 'th'
    return f"{n}{suffix}"


def get_date_in_words(date_obj):
    day = date_obj.day
    month = date_obj.strftime('%B')  # e.g. April
    year = date_obj.year

    # Convert day to ordinal (1st, 2nd, 3rd...)
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    return f"{day}{suffix} {month} {year}"


def download(student_id):
    student = Student.objects.get(student_id=student_id)
    className = student.class_name
    term = Term.objects.order_by('term_id').last()
    grades = Grade.objects.filter(student=student.student_id)
    total_score = total_score = sum(
    float(i.total_mark) for i in grades
    if i.total_mark and i.total_mark.replace('.', '', 1).isdigit()
)
    class_id = className.class_id
    ranked_students = (
        Student.objects.filter(class_name_id=class_id)
        .annotate(
            total_score=Sum(Cast('grade__total_mark', output_field=IntegerField())),
        )
        .annotate(
            position=Window(
                expression=Rank(),
                order_by=F('total_score').desc()
            )
        )
        .order_by('position')
    )
    student = ranked_students.filter(student_id=student_id).first()

    from collections import defaultdict

    position_map = defaultdict(dict)

    for g in grades:
        subject_id = g.subject_id

        rankings = (
            Grade.objects.filter(
                student__class_name_id=g.student.class_name_id,
                subject_id=subject_id
            )
            .annotate(
                numeric_score=Cast('total_mark', IntegerField())
            )
            .annotate(
                position=Window(
                    expression=Rank(),
                    order_by=F('numeric_score').desc()
                )
            )
            .values('student_id', 'subject_id', 'position')
        )

        for rank in rankings:
            position_map[rank['student_id']][rank['subject_id']] = rank['position']

    class PDF(FPDF):

        def header(self):
            self.image("mainApp/logo.png", x=5, y=10, w=30)  # School logo

            # Photo box (right corner)
            self.set_line_width(1)
            self.rect(x=175, y=10, w=25, h=30)

            # School info
            self.set_xy(0, 10)
            self.set_font("Arial", "B", 16)
            self.set_text_color(102, 0, 204)
            self.cell(0, 8, safe_text("PEACE EDUCATIONAL SCHOOL"), align="C", ln=True)

            self.set_font("Arial", "B", 12)
            self.set_text_color(0, 0, 0)
            self.cell(0, 6, safe_text("Early childhood Development Centre/Primary & Junior High school)"), align="C", ln=True)

            self.set_font("Arial", "B", 11)
            self.cell(0, 6, safe_text("MOTTO: KNOWLEDGE IS POWER."), align="C", ln=True)
            self.cell(0, 6, safe_text("P.O.BOX 12668, ACCRA - NORTH-GHANA"), align="C", ln=True)
            self.cell(0, 6, safe_text("TEL: 0204-072-719 / 0277-498-076"), align="C", ln=True)

            self.ln(2)
            self.set_font("Arial", "B", 14)
            self.set_text_color(102, 0, 204)
            self.cell(0, 8, safe_text(f"TERMINAL REPORT FOR {className.class_name}"), ln=True, align="C")
            self.ln(2)

        def footer(self):
            self.set_y(-15)
            self.set_font("Arial", "I", 8)
            self.cell(0, 10, safe_text(f"Page {self.page_no()}"), align="C")

    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # === STUDENT INFO ===
    pdf.set_font("Arial", "B", 12)

    pdf.set_text_color(0, 0, 102)
    pdf.cell(15, 8, "NAME:", ln=0)
    pdf.set_text_color(0, 204, 255)
    pdf.cell(80, 8, f"{student.student_f_name} {student.student_l_name}", ln=0)

    pdf.set_text_color(0, 0, 102)
    pdf.cell(15, 8, "TERM:", ln=0)
    pdf.set_text_color(0, 204, 255)
    pdf.cell(30, 8, f"{term.term_type}", ln=0)

    pdf.set_text_color(0, 0, 102)
    pdf.cell(45, 8, "POSITION IN CLASS:", ln=0)
    pdf.set_text_color(0, 204, 255)
    pdf.cell(0, 8, f"{number_to_ordinal(student.position)}", ln=1)

    pdf.set_text_color(0, 0, 102)
    pdf.cell(17, 8, "CLASS:", ln=0)
    pdf.set_text_color(0, 204, 255)
    pdf.cell(25, 8, f"{shorten_level_name(className.class_name)}", ln=0)

    pdf.set_text_color(0, 0, 102)
    pdf.cell(25, 8, "VACATION:", ln=0)
    pdf.set_text_color(0, 204, 255)
    pdf.cell(52, 8, f"{get_date_in_words(term.vacation_date)}", ln=0)

    pdf.set_text_color(0, 0, 102)
    pdf.cell(30, 8, "RE-OPENING:", ln=0)
    pdf.set_text_color(0, 204, 255)
    pdf.cell(30, 8, f"{get_date_in_words(term.reopen_date)}", ln=1)

    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)


    # === SUBJECT TABLE ===
    # Table header
    pdf.set_font("Arial", "B", 12,)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)

    # Add line breaks for multi-word headers
    pdf.set_font("Arial", "B", 12)
    pdf.set_text_color(0, 0, 0)
    pdf.set_fill_color(255, 255, 255)

    headers = [
        "SUBJECT\n ",
        "CLASS\nSCORE",
        "EXAMS\nSCORE",
        "TOTAL\n ",
        "POSITION\n ",
        "REMARKS\n "
    ]
    widths = [60, 25, 25, 20, 25, 35]

    # Get current position
    x_start = pdf.get_x()
    y_start = pdf.get_y()

    # Loop through headers and manually set x/y for each multi_cell
    for i in range(len(headers)):
        pdf.set_xy(x_start, y_start)  # reset to the top of the row
        pdf.multi_cell(widths[i], 5, safe_text(headers[i]), border=1, align="C", fill=True)
        x_start += widths[i]  # move x to the right for the next cell

    pdf.set_y(y_start + 10)# Move down after the header row



    # Table data
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 0)
    data = [
        (
            grade.subject.subject_name,
            grade.class_mark or "",
            grade.exams_mark or "",
            grade.total_mark or "",
            number_to_ordinal(position_map.get(grade.student_id, {}).get(grade.subject_id, "")),  # Position
            grade.remarks or ""
        )
        for grade in grades
    ]

    fill = False
    for row in data:
        for i in range(len(row)):
            pdf.set_fill_color(240, 240, 240) if fill else pdf.set_fill_color(255, 255, 255)
            pdf.cell(widths[i], 10, safe_text(row[i]), border=1, align="C", fill=True)
        fill = not fill  # Alternate row colors
        pdf.ln()

    pdf.ln(10)

    # === SUMMARY SECTION ===
    pdf.set_font("Arial", "B", 12)
    text = f"TOTAL SCORE = {total_score} / {grades.count()*100}"
    text_width = pdf.get_string_width(text)
    pdf.cell(0, 8, text, ln=True, align="C")
    pdf.ln(10)

    summary_items = [
        ("ATTENDANCE", f"{student.attendance} OUT OF {term.total_attendance}"),
        ("CONDUCT/CHARACTER", f"{student.conduct}"),
        ("INTEREST", f"{student.interest}"),
        ("CLASS TEACHER'S REMARKS", f"{student.remarks}"),
    ]

    for label, value in summary_items:
        pdf.set_text_color(0, 0, 102)
        pdf.cell(70, 8, f"{label}:", ln=0)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 8, value, ln=1)

    pdf.ln(5)
    pdf.cell(0, 8, "HEAD TEACHER'S SIGNATURE: _______________________________", ln=True)
    pdf.ln(10)

    # === GRADING SYSTEM ===
    # === GRADING SYSTEM ===
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "GRADING SYSTEM", ln=True)
    pdf.set_font("Arial", "", 10)

    grading = [
        ("80-100%", "EXCELLENT"),
        ("70-79%", "VERY GOOD"),
        ("60-69%", "GOOD"),
        ("45-59%", "CREDIT"),
        ("35-44%", "PASS"),
        ("0-34%", "WEAK PASS"),
    ]

    # Display in 2 columns
    for i in range(0, len(grading), 2):
        for j in range(2):
            if i + j < len(grading):
                score, grade = grading[i + j]
                pdf.cell(30, 6, score, ln=0)
                pdf.cell(50, 6, f"-- {grade}", ln=0)
        pdf.ln(6)  # Move to next line after each pair


    # Save the PDF
    output_path = f"terminal_report_of_{student.student_f_name}_{student.student_l_name}.pdf"
    pdf.output(output_path)
    return output_path