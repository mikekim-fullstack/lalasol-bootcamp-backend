from django.urls import path, include
from api.views import *
urlpatterns = [
    # Teachers
    path('teacher/', TeacherListsView.as_view()),
    path('teacher/<int:pk>/', TeacherDetailView.as_view()),
    path('teacher-login/', TeacherLogin),
    path('teacher-courses/<int:teacher_id>', TeacherCourseListsView.as_view()),
    path('teacher-course-detail/<int:pk>', CourseDetailView.as_view()),
    path('teacher-course-update/<int:pk>', CourseUpdateView.as_view()),
    
    # Courses
    path('course-category/', CourseCategoryListsView.as_view()),
    path('course-category-detail/<int:pk>', CourseCategoryDetailView.as_view()),
    
    
    path('courses-depth1/', AllCourseDepth1ListsView.as_view()),# depth=1



    # -- Fetch all courses by teacherID and catID --
    path('courses-all-by-teacher-cat/<int:teacher_id>/<int:cat_id>', CoursListsByTeacherAndCat.as_view()),
    # -- Fetch all courses by teacher ID --
    path('courses-all-by-teacher/<int:teacher_id>', CourseListsByTeacher.as_view()),

    # -- Fetch all courses with enrollment status with student ID --
    path('courses-enrolled-status/<int:student_id>', fetch_courses_with_enrolled_student_id),

    # -- Delete course with course ID. It can be deleted by any one so later it should be restricecd by teacher. ---
    path('course-delete/<int:pk>', CourseDeleteView.as_view()),

    # -- Update Course with course ID. ---
    path('course-update/<int:pk>', CourseUpdateView.as_view()),
    # -- Create Course by Teacher ID
    path('courses-create/', CourseCreateView.as_view()),

    # path('courses-search/<str:search>', AllCourseListsView.as_view()),
    path('course/<int:pk>', CourseDetailView.as_view()),#all

    # Chapters
    path('chapters/', ChapterListsView.as_view()),
    path('chapter/<int:pk>', ChapterDetailView.as_view()),
    path('course-chapter/<int:course_id>', CourseChapterListsView.as_view()),

    # Content
    path('chapter-content/', ChapterContentListsView.as_view()),
    path('chapter-content/<int:pk>', ChapterContentDetailView.as_view()),#for retrive and update content...
    path('chapter-content-add/', ChapterAddContentView.as_view()),
    path('chapter-content-delete/', ChapterDeleteContentView.as_view()),
    # path('chapter-content-update/', ChapterUpdateView.as_view()),
    path('chapters-content-viewed/', set_chapter_content_viewed),
    path('chapters-viewed/', get_chapter_viewed),
    path('chapter-category/', ChapterCategoryListsView.as_view()),
    # path('chapters-viewed/<int:student_id>/<int:chapter_id>', get_chapter_viewed),

    #Students
    path('student/', StudentListsView.as_view()),
    path('student-signup/', StudentSignUp),
    path('student-login/', StudentLogin),
    path('student/<int:pk>/', StudentDetailView.as_view()),
    
    path('manage-student-enroll-course/<int:student_id>/<int:cat_id>', manage_student_enroll_course),
    path('student-course-enrollment/', StudentCourseEnrollmentLists.as_view()),
    path('student-course-enrollment/<int:student_id>', fetch_enrolled_courses_by_student_id),
    path('student-course-enrollment/<int:student_id>/<int:category_id>', fetch_enrolled_courses_by_student_id_n_cat_id),
    path('fetch-enroll-status/<int:course_id>/<int:student_id>/', fetch_enroll_status),
    path('fetch-enrolled-students/',EnrolledStudentLists.as_view()),
    path('fetch-viewed-chapters-bycourse/', fetch_viewed_chapters_by_course_id),
    # path('fetch-enrolled-student-with/<int:course_id>/',EnrolledStudentLists.as_view()),
    # path('fetch-enrolled-teacher-with/<int:teacher_id>/',EnrolledStudentLists.as_view()),
    path('course-rating/', CourseRatingLists.as_view()), 
    path('course-rating/<int:course_id>/', CourseRatingLists.as_view()), 
    path('fetch-rating-status/<int:student_id>/<int:course_id>/', fetch_rating_status)

]