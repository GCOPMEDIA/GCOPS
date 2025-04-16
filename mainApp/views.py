from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse
from .models import *
from .utils import download
# Create your views here.

def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Try to get the 'next' parameter from either GET or POST
        next_url = request.GET.get('next') or request.POST.get('next')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(next_url) if next_url else redirect('teacher_view')  # Redirect to next URL or default
        else:
            return HttpResponse(status=403)  # Or render with an error message

    next_url = request.GET.get('next', '')  # Preserve 'next' parameter for redirection
    return render(request, 'registration/login.html', {'next': next_url})

def teacher_view(request):
    return render(request,'teacher.html')

def add_student(request):
    classes =  ClassName.objects.all()
    if request.method == "POST":
        f_name = request.POST.get('studentFName')
        l_name = request.POST.get('studentLName')
        class_id = request.POST.get("class")
        selected_class = ClassName.objects.get(class_id=class_id)

        # Save student (you can fill this in)
        Student.objects.create(student_f_name=f_name, student_l_name=l_name, class_name=selected_class)

        return render(request, "done_registering.html", {
            "student_name": f"{f_name} {l_name}",
            "class_name": selected_class.class_name
        })

    return render(request,"student.html",{"classes":classes})

def class_view(request):
    class_= ClassName.objects.get(teacher=request.user.id)
    students = Student.objects.filter(class_name=class_)

    return render(request, 'class.html', {'students': students})


    # Add grade logic goes here...


from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Subject, Grade

def add_grade(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    subjects = Subject.objects.all()

    if request.method == "POST":
        for subject in subjects:
            class_mark = request.POST.get(f'class_mark_{subject.subject_id}')
            exams_mark = request.POST.get(f'exams_mark_{subject.subject_id}')

            if not class_mark or not exams_mark:
                continue

            class_mark = int(class_mark)
            exams_mark = int(exams_mark)
            total = class_mark + exams_mark

            # Determine remark based on total
            if total >= 80:
                remark = "EXCELLENT"
            elif total >= 70:
                remark = "VERY GOOD"
            elif total >= 60:
                remark = "GOOD"
            elif total >= 45:
                remark = "CREDIT"
            elif total >= 35:
                remark = "PASS"
            else:
                remark = "WEAK PASS"

            Grade.objects.create(
                class_mark=class_mark,
                exams_mark=exams_mark,
                total_mark=total,
                remarks=remark,
                student=student,
                subject=subject
            )

        # Get extra details
        conduct = request.POST.get("conduct")
        attendance = request.POST.get("attendance")
        interest = request.POST.get("interest")
        overall_remarks = request.POST.get("overall_remarks")

        # Update student record
        student.conduct = conduct
        student.attendance = attendance
        student.interest = interest
        student.remarks = overall_remarks
        student.graded = True
        student.save()

        return redirect("class_view")  # or wherever you want to redirect

    return render(request, 'grade.html', {'student': student, 'subjects': subjects})
def view_grade(request, student_id):
    student = get_object_or_404(Student, student_id=student_id)
    grades = Grade.objects.filter(student=student).select_related('subject')

    return render(request, 'view_grade.html', {
        'student': student,
        'grades': grades
    })

from django.shortcuts import render, get_object_or_404, redirect
from .models import Grade

def edit_single_grade(request, grade_id):
    grade = get_object_or_404(Grade, grade_id=grade_id)

    if request.method == 'POST':
        class_mark = request.POST.get('class_mark')
        exams_mark = request.POST.get('exams_mark')

        # Calculate total mark
        try:
            class_mark_int = int(class_mark)
            exams_mark_int = int(exams_mark)
        except ValueError:
            return HttpResponse("Please enter valid numbers", status=400)

        total = class_mark_int + exams_mark_int

        # Grading system
        if total >= 80:
            remark = "EXCELLENT"
        elif total >= 70:
            remark = "VERY GOOD"
        elif total >= 60:
            remark = "GOOD"
        elif total >= 45:
            remark = "CREDIT"
        elif total >= 35:
            remark = "PASS"
        else:
            remark = "WEAK PASS"

        # Save updates
        grade.class_mark = class_mark
        grade.exams_mark = exams_mark
        grade.total_mark = str(total)
        grade.remarks = remark
        grade.save()

        return redirect('view_grade', student_id=grade.student.student_id)

    return render(request, 'edit_grade.html', {'grade': grade})
def download_grade_pdf(request,student_id):
    output_path = download(student_id)
    with open(output_path, 'rb') as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="member_{student_id}.pdf"'
        return response




