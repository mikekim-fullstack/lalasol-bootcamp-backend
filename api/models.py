from django.db import models

from re import T
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.serializers import serialize
import cv2
from account.models import UserAccount
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField, PPOIField
from django.conf import settings
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.gis.db.models.functions import Distance
from django.db.models import F

'''---------------------------------------------------''' 


class CourseCategory(MPTTModel):
    title=models.CharField(max_length=150)
    description=models.TextField()
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(max_length = 100, unique=True)
    popularity = models.SmallIntegerField(default=0)
    image_max_number = models.SmallIntegerField(default=10)
    post_validity_in_day = models.SmallIntegerField(default=30)
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
        order_insertion_by = ['name',]

# ---- Students -----
class Student(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='user_student')
    # full_name=models.CharField(max_length=100)
    # email=models.CharField(max_length=100, unique=True)
    # password=models.CharField(max_length=100)
    # username=models.CharField(max_length=200)
    interested_categories=models.ManyToManyField(CourseCategory, related_name='cat_student')
    profile_img = models.ImageField(upload_to='student_profile_imgs/', null=True)

    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = '1. Students'
    def __str__(self):
        return self.full_name
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
    full_name=models.CharField(max_length=100)
    bio=models.TextField(null=True)
    email=models.CharField(max_length=100, unique=True)
    password=models.CharField(max_length=100)
    qualification=models.CharField(max_length=200)
    mobile_no=models.CharField(max_length=20)
    skills=models.TextField()
    photo = models.ImageField(upload_to='teacher_imgs', null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name_plural = '2. Teachers'
    def __str__(self):
        return self.full_name
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
    techs=models.TextField(null=True)
    course_views = models.IntegerField(default=0, null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name_plural = '4. Courses'
    def __str__(self):
        return self.title
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

class Chapter(models.Model):
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_chapters')
    title=models.CharField(max_length=150)
    description=models.TextField()
    video=models.FileField(upload_to='chapter_videos/', null=True)
    remarks=models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)
    class Meta:
        verbose_name_plural = '6. Chapter'
    def __str__(self):
        return self.title
    def chapter_duration(self):
        cap = cv2.VideoCapture(self.video.path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration=0
        if frame_count:
            duration = frame_count/fps
        return duration

# ----------------------------------------------------------------

# Student  enrolled courses
class StudentEnrolledCourse(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course=models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
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
