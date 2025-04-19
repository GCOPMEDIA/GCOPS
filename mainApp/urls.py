from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('',login_,name="login_"),
    path('teacher_view/',teacher_view,name="teacher_view"),
    path("add-student/",add_student,name="add_student"),
    path("class-view/",class_view,name="class_view"),
    path('add-grade/<int:student_id>/', add_grade, name='add_grade'),
    path('view_grade/<int:student_id>/',view_grade,name='view_grade'),
path('edit-grade/<int:grade_id>/', edit_single_grade, name='edit_single_grade'),
    path('download-pdf/<int:student_id>/',download_grade_pdf,name='download_grade_pdf'),
    path("all-classes",allClasses,name="allClasses"),
    path("all-students/<class_id>/",classView,name="classView")



]
