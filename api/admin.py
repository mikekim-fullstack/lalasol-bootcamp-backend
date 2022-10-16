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

# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'notif_subject', 'notif_for', 'notifread_status']
# admin.site.register(Notification, NotificationAdmin)
# admin.site.register(Quiz)
# admin.site.register(QuizQuestion)
# admin.site.register(CourseQuiz)
# admin.site.register(AttemptQuiz)
# admin.site.register(StudyMaterial)
