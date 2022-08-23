from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to="course_covers/")
    creation_date = models.DateTimeField(auto_now_add=True)
    duration = models.CharField(max_length=300, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    favourite = models.ManyToManyField(User, related_name='favourite', blank=True)


class CourseFile(models.Model):
    files = models.FileField(upload_to="course_files/")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.files)


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    question = models.CharField(max_length=600)
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    cat = (('Option1', 'Option1'), ('Option2', 'Option2'), ('Option3', 'Option3'), ('Option4', 'Option4'))
    answer = models.CharField(max_length=200, choices=cat)

    def __str__(self):
        return f"{self.course}+{self.question}"
