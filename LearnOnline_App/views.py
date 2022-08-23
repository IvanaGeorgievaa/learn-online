import datetime
import os

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, FileResponse, Http404, HttpResponse

from .models import Course, UserCourse, Question, CourseFile
from .forms import CreateUserForm, CourseForm, FilesForm, QuestionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from .process import html_to_pdf


# Create your views here.
def home(request):
    return render(request, "home.html")


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

    context = {'form': form}
    return render(request, "register.html", context=context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, "login.html", context)


def logout_user(request):
    logout(request)
    return redirect('login')


def courses(request):
    query = Course.objects.all()

    p = Paginator(Course.objects.all(), 6)
    page = request.GET.get('page')
    courses_list = p.get_page(page)

    context = {"courses": query, "courses_list": courses_list}
    return render(request, "courses.html", context=context)


@login_required(login_url='/login')
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("courses")
    context = {"form": CourseForm}
    return render(request, "addCourse.html", context=context)


@login_required(login_url='/login')
def update_course(request, pk):
    course = Course.objects.get(id=pk)
    form = CourseForm(request.POST or None, instance=course)
    context = {"course": course, "form": form}
    if form.is_valid():
        form.save()
        return redirect("courseDetails", pk=course.id)
    return render(request, "updateCourse.html", context=context)


@login_required(login_url='/login')
def delete_course(request, pk):
    course = Course.objects.get(id=pk)
    course.delete()
    return redirect("courses")


def add_files_to_course(request, pk):
    course = Course.objects.get(id=pk)
    if request.method == 'POST':
        form = FilesForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.course = course
            post.save()
            return redirect("courseDetails", pk=course.id)
    context = {"form": FilesForm, "course": course}
    return render(request, "AddFilesToCourse.html", context=context)


def delete_file_from_course(request, pkc, pkf):
    course = Course.objects.get(id=pkc)
    all_course_files = CourseFile.objects.filter(course=course)
    file_to_delete = all_course_files.get(id=pkf)
    file_to_delete.delete()
    return redirect("courseDetails", pk=course.id)


def search_course(request):
    query = request.GET['query']
    searched_course = Course.objects.filter(title__icontains=query)
    context = {"searched_course": searched_course, "query": query}
    return render(request, "search_courses.html", context=context)


@login_required(login_url='/login')
def course_details(request, pk):
    course = Course.objects.get(id=pk)
    course_id = Course.objects.get(id=pk)
    files = CourseFile.objects.filter(course=course)
    try:
        check_enroll = UserCourse.objects.get(user=request.user, course=course_id)
    except UserCourse.DoesNotExist:
        check_enroll = None

    context = {'course': course, 'check_enroll': check_enroll, 'files': files}
    return render(request, 'courseDetails.html', context=context)


def pdf_view(request, pkc, pkf):
    course = Course.objects.get(id=pkc)
    all_course_files = CourseFile.objects.filter(course=course)
    file_to_open = all_course_files.get(id=pkf)
    path = os.path.join(settings.MEDIA_ROOT, str(file_to_open.files))
    try:
        return FileResponse(open(str(path), 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()


@login_required(login_url='/login')
def start_exam(request, pk):
    course = Course.objects.get(id=pk)
    questions = Question.objects.all().filter(course=course)
    if request.method == 'POST':
        pass
    response = render(request, 'start_exam.html', {'course': course, 'questions': questions})
    response.set_cookie('course_id', course.id)
    return response


@login_required(login_url='/login')
def add_question(request, pk):
    course = Course.objects.get(id=pk)
    question_form = QuestionForm()
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.course = course
            question.save()
        else:
            print("form is invalid")
        return redirect("courseDetails", pk=course.id)
    return render(request, 'add_question.html', {'form': question_form, 'course': course})


@login_required(login_url='/login')
def delete_question(request, pkc, pkq):
    course = Course.objects.get(id=pkc)
    question = Question.objects.get(id=pkq)
    question.delete()
    return redirect("start_exam", pk=course.id)


@login_required(login_url='/login')
@csrf_exempt
def certificate(request, pk):
    course = Course.objects.get(id=pk)
    context = {"course": course}
    if request.method == 'POST':
        pass
    return render(request, 'certificate.html', context=context)


@login_required(login_url='/login')
def enroll(request, pk):
    course = Course.objects.get(id=pk)
    create_course = UserCourse(
        user=request.user,
        course=course
    )
    create_course.save()
    return redirect('my-courses')


def remove_enroll(request, pk):
    course = UserCourse.objects.get(id=pk)
    course.delete()
    return redirect('my-courses')


@login_required(login_url='/login')
def my_courses(request):
    course = UserCourse.objects.filter(user=request.user)
    context = {'course': course}
    return render(request, 'my_courses.html', context=context)


@login_required(login_url='/login')
def favourite_course(request, pk):
    course = get_object_or_404(Course, id=pk)
    if course.favourite.filter(id=request.user.id).exists():
        course.favourite.remove(request.user)
    else:
        course.favourite.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required(login_url='/login')
def course_favourite_list(request):
    user = request.user
    favourite_courses = user.favourite.all()
    context = {
        'favourite_courses': favourite_courses,
    }
    return render(request, 'course_favourite_list.html', context)


@login_required(login_url='/login')
def get_certificate(request):
    user = request.user
    date = datetime.date.today()
    pdf = html_to_pdf('certificate_file.html', {"date": date, "user": user})

    # rendering the template
    return HttpResponse(pdf, content_type='application/pdf')
