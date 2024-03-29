from django.contrib import admin

from api.models import *
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','bio',  'qualification',  'skills']
    list_display_links= ['id', 'user']

class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'teacher', 'description']
    list_display_links = ['id', 'title']

class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'chapter_no','course', 'description']
    list_display_links = ['id', 'name']

class ChapterContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'chapter_category','title','content_no', 'creator', 'image','file', 'url', 'text']
    list_display_links = ['id','title',]

class ChapterContentCommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'chapter_content','user','comment','created_date','updated_date']
    list_display_links = ['id','chapter_content','user',]

class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'description')
    list_display_links = ['id', 'title']

class StudentCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','user', 'team', 'status')
    list_display_links = ['id', 'user']

class ChapterCategoryAdmin(admin.ModelAdmin):
    list_display = ('id','title','seq_no', 'created_date')
    list_display_links = ['id', 'title', 'seq_no']

class StudentChapterContentViewedAdmin(admin.ModelAdmin):
    list_display = ('id','student', 'chapter', 'content', 'viewed','viewed_date')
    list_display_links = ['id', 'content']

class JavaScriptCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student','teacher', 'title', 'js_code')
    list_display_links=('id', 'title')

class HtmlCodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'student','teacher', 'title', 'js_code')
    list_display_links=('id', 'title')

admin.site.register(Teacher, TeacherAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Chapter, ChapterAdmin)
admin.site.register(ChapterContent, ChapterContentAdmin)
admin.site.register(ChapterContentComment, ChapterContentCommentAdmin)
admin.site.register(StudentChapterContentViewed, StudentChapterContentViewedAdmin)
admin.site.register(ChapterCategory, ChapterCategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentCategoryAdmin)
admin.site.register(StudentEnrolledCourse)
admin.site.register(CourseRating)
admin.site.register(StudentFavoriteCourse)
admin.site.register(StudentAssignment)
admin.site.register(Team)
admin.site.register(ClassRoom)
admin.site.register(JavaScriptCode, JavaScriptCodeAdmin)
admin.site.register(HtmlCode, HtmlCodeAdmin)
# class NotificationAdmin(admin.ModelAdmin):
#     list_display = ['id', 'notif_subject', 'notif_for', 'notifread_status']
# admin.site.register(Notification, NotificationAdmin)
admin.site.register(InputQuizType)
admin.site.register(OfferedAnswer)
# admin.site.register(OfferedQuizAnswers)
admin.site.register(CourseCategoryQuiz)
admin.site.register(StudentQuizSolution)
# admin.site.register(StudyMaterial)
