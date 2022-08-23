from django import forms
from django.contrib.auth.models import User
from .models import Course, CourseFile, Question
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = 'form-control'

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = 'form-control'

    class Meta:
        model = Course
        exclude = ("author",)


class FilesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FilesForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = 'form-control'

    class Meta:
        model = CourseFile
        exclude = ("course",)


class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = 'form-control'

    class Meta:
        model = Question
        exclude = ("course", )
