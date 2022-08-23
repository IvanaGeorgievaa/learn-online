"""Dnick_Proekt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve


from LearnOnline_App.views import courses, home, register, login_page, logout_user, \
    course_details, favourite_course, course_favourite_list, search_course, enroll, \
    my_courses, remove_enroll, pdf_view, start_exam, certificate, get_certificate,\
    add_course, add_files_to_course, delete_course, delete_file_from_course,\
    update_course, add_question, delete_question
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register, name='register'),
    path('login/', login_page, name='login'),
    path('logout/', logout_user, name='logout'),
    path('home/', home, name="home"),
    path('courses/', courses, name="courses"),
    path('add/course/', add_course, name="addCourse"),
    path('update/course/<str:pk>/', update_course, name="updateCourse"),
    path('delete/course/<str:pk>/', delete_course, name="deleteCourse"),
    path('add/files/<str:pk>/', add_files_to_course, name="addFiles"),
    path('delete/file/<str:pkc>/<str:pkf>/', delete_file_from_course, name="deleteFile"),
    path('courses/<str:pk>/', course_details, name="courseDetails"),
    path('search_course/', search_course, name="search-course"),
    path('enroll/<str:pk>/', enroll, name="enroll"),
    path('remove_enroll/<str:pk>/', remove_enroll, name="remove_enroll"),
    path('my_courses', my_courses, name="my-courses"),
    path('favourite_course/<str:pk>/', favourite_course, name="favourite_course"),
    path('favourites/', course_favourite_list, name="course_favourite_list"),
    path('pdf_view/<str:pkc>/<str:pkf>/', pdf_view, name="pdf_view"),
    path('start_exam/<str:pk>/', start_exam, name="start_exam"),
    path('add-question/<str:pk>/', add_question, name='addQuestion'),
    path('delete-question/<str:pkc>/<str:pkq>/', delete_question, name='deleteQuestion'),
    path('certificate/<str:pk>/', certificate, name="certificate"),
    path('pdf/', get_certificate, name="get_certificate"),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT})
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
