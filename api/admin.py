from django.contrib import admin

from api.models import *
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','bio',  'qualification',  'skills']
    list_display_links= ['id', 'user']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher', 'description']
    list_display_links = ['id', 'title']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'course', 'description']
    list_display_links = ['id', 'title']

class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description')
    list_display_links = ['id', 'title']

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student)
admin.site.register(StudentEnrolledCourse)
admin.site.register(CourseRating)
admin.site.register(StudentFavoriteCourse)
admin.site.register(StudentAssignment)
admin.site.register(ChapterCategory)
admin.site.register(Team)
admin.site.register(ClassRoom)

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'notif_subject', 'notif_for', 'notifread_status']
# admin.site.register(Notification, NotificationAdmin)
admin.site.register(InputQuizType)
admin.site.register(OfferedAnswer)
# admin.site.register(OfferedQuizAnswers)
admin.site.register(CourseCategoryQuiz)
admin.site.register(StudentQuizSolution)
# admin.site.register(StudyMaterial)
