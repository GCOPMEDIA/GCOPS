from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.http import HttpResponse
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
    if request.method == "POST":
        f_name = request.POST.get('studentFName')
        l_name = request.POST.get('studentLName')
        class_ = request.POST.get("class")
        print(f_name,l_name,class_)
        return HttpResponse(f"{f_name} {l_name} is in class {class_}", status=200)
    return render(request,"student.html")

def class_view(request):
    print(request.user)
    return render(request, 'class.html', {'user': request.user})



