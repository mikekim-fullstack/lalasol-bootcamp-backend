from email.policy import default
from enum import unique
from secrets import choice
from django.db import models
import os

from re import T
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.serializers import serialize
# --- import cv2
from account.models import UserAccount
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
# --- from versatileimagefield.fields import VersatileImageField, PPOIField
from django.conf import settings
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.gis.db.models.functions import Distance
from django.db.models import F

'''---------------------------------------------------''' 
# def remove_field(model_cls, field_name):
#     for field in model_cls._meta.local_fields:
#         if field.name == field_name:
#             model_cls._meta.local_fields.remove(field)
'''---------------------------------------------------''' 


class CourseCategory(MPTTModel):
    title=models.CharField(max_length=150)
    description=models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length = 100, unique=True)
    popularity = models.SmallIntegerField(default=0)
    image_max_number = models.SmallIntegerField(default=10)
    post_validity_in_day = models.SmallIntegerField(default=30)
    order = models.PositiveSmallIntegerField(null=True,unique=True) # category order to display
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = '3. Course Categories'
    def __str__(self):     
        '''
        a=['a','b','c']
        a[::-1] #reverse list/tuple/string
        >>> ['c', 'b', 'a']
        '->'.join(a[::-1]) #join with '->'
        >>> 'c->b->a'
        '''                      
        # full_path = [self.name]            
        # k = self.parent
        # while k is not None:
        #     full_path.append(k.name)
        #     k = k.parent
        # return ' -> '.join(full_path[::-1])

        return self.title

    class MPTTMeta:
        order_insertion_by = ['title',]

class ChapterCategory(models.Model):
    title=models.CharField(max_length=150)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        verbose_name_plural = '3-1. Chapter Categories'
    def __str__(self):     
        return self.title

#------- Team -----------------
class Team(models.Model):
    name=models.CharField(max_length=100)
    added_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
# ---- Students -----
# TRIGGER FUNCTION
# def student_file_upload(instance, filename):
#     'student_profile_imgs/'
#     instance.file.open() # make sure we're at the beginning of the file
#         contents = instance.file.read() # get the contents
#         fname, ext = os.path.splitext(filename)
#         return "'chapter_files/'{0}_{1}{2}".format(fname, hash(contents), ext)
#     pass
class Student(models.Model):
    STATUS=[
        ('STUDENT',  'STUDENT'),
        ('GRADUATE', 'GRADUATE'),
        ('AUDIT',    'AUDIT'),
    ]
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_student')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_student', null=True, blank=True)
    # interested_categories=models.ManyToManyField(CourseCategory, related_name='cat_student')
    profile_img = models.ImageField(upload_to='student_profile_imgs/', null=True, blank=True)
    status = models.CharField(max_length=10, null=True, choices=STATUS, default=STATUS[0][0])
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    end_date = models.DateTimeField( null=True)
    class Meta:
        verbose_name_plural = '1. Students'
    def __str__(self):
        return self.user.first_name+' '+self.user.last_name
    
    def enrolled_courses(self):
        '''
        Total enrolled course by student.
        '''
        return StudentEnrolledCourse.objects.filter(student=self).count()
    def favorite_courses(self):
        '''
        Total favorite courses by student.
        '''
        return StudentFavoriteCourse.objects.filter(student=self).count()
    def complete_assigments(self):
        '''
        Total completed assignments by student.
        '''
        return StudentAssignment.objects.filter(student=self, student_status=True).count()
    def pending_assigments(self):
        '''
        Total pending assignments by student.
        '''
        return StudentAssignment.objects.filter(student=self, student_status=False).count()

# ---- Teacher -----
class Teacher(models.Model):
    STATUS=[
        ('EMPLOYEE',  'EMPLOYEE'),
        ('EXEMPLOYEE', 'EXEMPLOYEE'),
        ('PARTTIME',    'PARTTIME'),
    ]
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_teacher')
    team = models.ManyToManyField(Team,  related_name='team_teacher')
    qualification=models.CharField(max_length=200)
    bio=models.TextField(null=True)
    skills=models.TextField()
    status = models.CharField(max_length=12, choices=STATUS, default=STATUS[0][0], null=True)
    photo = models.ImageField(upload_to='teacher_imgs', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    end_date = models.DateTimeField( null=True)

    class Meta:
        verbose_name_plural = '2. Teachers'
    def __str__(self):
        return self.user.get_full_name()
    def skill_lists(self):
        skill_lists = self.skills.split(',')
        return [s.strip() for s in skill_lists]


# ----------------------------------------------------------------

class Course(models.Model):
    category=models.ForeignKey(CourseCategory, on_delete=models.CASCADE, related_name='category_courses')
    teacher=models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_courses')
    title=models.CharField(max_length=150)
    description=models.TextField()
    course_image=models.ImageField(upload_to='course_imgs/', null=True)
    taken = models.BooleanField(default=False, null=True)
    course_no = models.PositiveSmallIntegerField(null=True, default=1)
    course_views = models.IntegerField(default=0, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name_plural = '4. Courses'
    def __str__(self):
        return (self.category.title +':'+self.title)
    def related_video(self):
        search = self.techs.split() 
        # print('Course: techs:', self.techs, search)
        # Q(Title__icontains = search)|Q(Title__icontains = x) for x in search
        '''
            q = Q(content__icontains=term_list[0]) | Q(title__icontains=term_list[0])
            for term in term_list[1:]:
                q.add((Q(content__icontains=term) | Q(title__icontains=term)), q.connector)
        '''
        q = Q(techs__icontains=search[0]) | Q(techs__icontains=search[0])
        for term in search[1:]:
                q.add((Q(techs__icontains=term) | Q(techs__icontains=term)), q.connector)
        rel_videos = Course.objects.filter(q)
        return serialize('json',rel_videos)
    def tech_lists(self):
        tech_lists = self.techs.split(',')
        # stripped = [s.strip() for s in my_list]
        # stripped = list(map(str.strip, my_list))
        tech_lists = [s.strip() for s in tech_lists]
        return tech_lists

    def total_enrolled_students(self):
        student_count = StudentEnrolledCourse.objects.filter(course=self).count()
        return student_count

    def course_rating(self):
        courses = CourseRating.objects.filter(course=self)
        if(courses):
            course_avg_rate = courses.aggregate(avg_rating=models.Avg('rating'))
            return course_avg_rate['avg_rating']
        return 0
#Course Rating and Reviews
class CourseRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_rating')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_rating')
    rating = models.PositiveSmallIntegerField(default=0)
    reviews = models.TextField(null=True)
    reviewed_date=models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = '5. Course Rating'
    def __str__(self):
        return f'rating:{self.course}-{self.student}-{self.rating}'

# TRIGGER FUNCTION
def hash_upload(instance, filename):
        instance.file.open() # make sure we're at the beginning of the file
        contents = instance.file.read() # get the contents
        fname, ext = os.path.splitext(filename)
        return "'chapter_files/'{0}_{1}{2}".format(fname, hash(contents), ext) # assemble the filename
#  ---------- ChapterContent ----------------
class ChapterContent(models.Model):
    chapter_category=models.ForeignKey(ChapterCategory, on_delete=models.CASCADE, related_name='chapterContents', related_query_name='chapterContent')
    creater = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='chapterContents', related_query_name='chapterContent')
    title = models.CharField(max_length=150, null=True, blank=True)
    file=models.FileField(upload_to=hash_upload, null=True, blank=True)
    url=models.URLField(max_length=200, null=True, blank=True)
    text=models.TextField(null=True, blank=True)
    content_no=models.PositiveSmallIntegerField(null=True, default=1)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        verbose_name_plural = '6.1 ChapterContent'
    def __str__(self):
        return str(self.id) +':'+self.chapter_category.title+'-'+self.creater.user.get_full_name()+'-'+str(self.content_no)
class Chapter(models.Model):
    content=models.ManyToManyField(ChapterContent, related_name='chapters',related_query_name='chapter')
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters',related_query_name='chapter', null=True)
    title=models.CharField(max_length=150, null=True, blank=True)
    sub_title=models.CharField(max_length=150, null=True, blank=True)
    chapter_no=models.PositiveSmallIntegerField(null=True, default=1)
    description=models.TextField(null=True, blank=True)
    # video=models.FileField(upload_to='chapter_videos/', null=True)
    # file=models.FileField(upload_to=hash_upload, null=True, blank=True)
    # url=models.URLField(max_length=200, null=True, blank=True)
    # text=models.TextField(null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        verbose_name_plural = '6. Chapter'
    def __str__(self):
        return self.title
    
    # def chapter_duration(self):
    #     cap = cv2.VideoCapture(self.video.path)
    #     fps = cap.get(cv2.CAP_PROP_FPS)
    #     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    #     duration=0
    #     if frame_count:
    #         duration = frame_count/fps
    #     return duration

# ----------------------------------------------------------------

# Student  enrolled courses
class StudentEnrolledCourse(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_enrolled_courses', related_query_name="student_enrolled_course")
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_enrolled_courses', related_query_name="course_enrolled_course",)
    enrolled_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural ='7. Student Enrolled Course'
    def __str__(self):
        return f'enrolled:{self.course }-{self.student}'

class StudentFavoriteCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_studentfavorite')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_studentfavorite')
    status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='8. Student Fovorite Courses'
    def __str__(self):
        return 'favorite: '+self.student+'-'+self.course

class StudentAssignment(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='teacher_assignment')
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_assignment')
    title = models.CharField( max_length=200)
    detail=models.TextField()
    student_status = models.BooleanField(default=False)
    added_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='9. Student Assignments'
    def __str__(self):
        return 'assignment: '+self.title

# ---------- Quiz -----------------

class InputQuizType(models.Model):
    type = models.CharField( max_length=20)
    class Meta:
        verbose_name_plural='20. InputQuizType'
    def __str__(self):
        return self.type

class OfferedAnswer(models.Model):
    course_category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE, related_name='course_offeredAnswer', null=True)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='teacher_offeredAnswer', null=True)
    number=models.PositiveSmallIntegerField(null=True)
    answer = models.CharField( max_length=150)
    class Meta:
        verbose_name_plural='21.OfferedAnswer'
    def __str__(self):
        return str( self.teacher)+'-'+str(self.course_category)+'-'+str(self.id)+'-'+str(self.number) +': '+ self.answer

# class OfferedQuizAnswers(models.Model):
#     teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='teacher_offeredQuizAnswers', null=True)
#     type = models.ForeignKey(InputQuizType, on_delete=models.CASCADE, related_name='type_offeredQuizAnswers')
#     course_category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE, related_name='course_offeredQuizAnswers', null=True)
#     answers = models.ManyToManyField( OfferedAnswer, related_name='answers_offeredQuizAnswers')

#     added_date = models.DateTimeField(auto_now_add=True)
#     class Meta:
#         verbose_name_plural='23. OfferedQuizAnswers'
#     def __str__(self):
#         return str(self.id)

class CourseCategoryQuiz(models.Model):
    '''
    Add quiz to Course
    '''
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='teacher_courseCategoryQuiz')
    course_category = models.ForeignKey(CourseCategory,on_delete=models.CASCADE, related_name='course_courseCategoryQuiz')
    input_type = models.ForeignKey(InputQuizType, on_delete=models.CASCADE, related_name='type_courseCategoryQuiz')
    # offered_answers = models.ForeignKey(OfferedQuizAnswers, on_delete=models.CASCADE, related_name='offeredAnswers_courseCategoryQuiz')
    offered_answers = models.ManyToManyField( OfferedAnswer, related_name='offeredAnswers_courseCategoryQuiz')
    question = models.CharField(max_length=300)
    right_answer = models.CharField(max_length=200)
    added_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='24. CourseCategoryQuiz'
    def __str__(self):
        return self.question
class StudentQuizSolution(models.Model):
    '''
    Add StudentQuizSolution
    '''
    gradeby  = models.ForeignKey(Teacher,on_delete=models.CASCADE, related_name='teacher_StudentQuizSolution', null=True, blank=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_StudentQuizSolution')
    course_cat_quiz = models.ForeignKey(CourseCategoryQuiz,on_delete=models.CASCADE, related_name='catquiz_StudentQuizSolution')
    answer = models.CharField(max_length=200, null=True, blank=True)
    taken = models.BooleanField(default=False, null=True, blank=True)
    feedback = models.CharField(max_length=200, null=True, blank=True)
    score = models.PositiveSmallIntegerField(null=True, blank=True)
    added_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural='24. StudentQuizSolution'
    def __str__(self):
        return self.student
# class StudentScore(models.Model):
#     student = models.ForeignKey(Student,on_delete=models.CASCADE, related_name='student_StudentScore')
#--------------- ClassRoom -------------------

class ClassRoom(models.Model):
    name=models.CharField(max_length=100)
   
    student = models.ManyToManyField(Student, related_name='student_classRoom')
    teacher = models.ManyToManyField(Teacher, related_name='teacher_classRoom')
    added_date = models.DateTimeField(auto_now_add=True)


