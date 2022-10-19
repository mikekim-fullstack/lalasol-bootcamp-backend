from django.urls import path, include
from api.views import *
urlpatterns = [
    # Teachers
    path('teacher/', TeacherListsView.as_view()),
    path('teacher/<int:pk>/', TeacherDetailView.as_view()),
    # path('teacher-login/', TeacherLogin),
    path('teacher-courses/<int:teacher_id>', TeacherCourseListsView.as_view()),
    path('teacher-course-detail/<int:pk>', CourseDetailView.as_view()),
    path('teacher-course-update/<int:pk>', CourseUpdateView.as_view()),
    
    # Courses
    path('course-category/', CourseCategoryListsView.as_view()),
    path('courses-create/', CourseCreateView.as_view()),
    path('courses/', AllCourseListsView.as_view()),
    path('courses-search/<str:search>', AllCourseListsView.as_view()),
    path('course/<int:pk>', CourseDetailView.as_view()),#all

    # Chapters
    path('chapters/', ChapterListsView.as_view()),
    path('chapter/<int:pk>', ChapterDetailView.as_view()),
    path('course-chapter/<int:course_id>', CourseChapterListsView.as_view()),

    #Students
    path('student/', StudentListsView.as_view()),
    # path('student-login/', StudentLogin),
    path('student/<int:pk>/', StudentDetailView.as_view()),
    path('student-course-enrollment/', StudentCourseEnrollmentLists.as_view()),
    path('fetch-enroll-status/<int:course_id>/<int:student_id>/', fetch_enroll_status),
    path('fetch-enrolled-students/',EnrolledStudentLists.as_view()),
    path('fetch-enrolled-students/',EnrolledStudentLists.as_view()),
    # path('fetch-enrolled-student-with/<int:course_id>/',EnrolledStudentLists.as_view()),
    # path('fetch-enrolled-teacher-with/<int:teacher_id>/',EnrolledStudentLists.as_view()),
    path('course-rating/', CourseRatingLists.as_view()), 
    path('course-rating/<int:course_id>/', CourseRatingLists.as_view()), 
    path('fetch-rating-status/<int:student_id>/<int:course_id>/', fetch_rating_status)

]