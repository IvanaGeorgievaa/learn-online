from django.contrib import admin

from .models import Course, Question, CourseFile


# Register your models here.
class CourseFileAdmin(admin.StackedInline):
    list_display = ('files',)
    model = CourseFile


class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'author')
    exclude = ('author',)
    inlines = (CourseFileAdmin,)

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Course, CourseAdmin)


def course_title(obj):
    return obj.course.title


class QuestionAdmin(admin.ModelAdmin):
    list_display = (course_title, 'question')


admin.site.register(Question, QuestionAdmin)
