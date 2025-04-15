from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('',login_,name="login_"),
    path('teacher_view/',teacher_view,name="teacher_view"),
    path("add-student/",add_student,name="add_student")
]
