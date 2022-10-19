from rest_framework import serializers
from api.models import *
# Teachers
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model=Teacher
        fields=['id', 'user', 'bio', 'qualification','skills','photo','created_date','updated_date']
        fields +=['skill_lists']
        fields +=['teacher_courses'] # techer.course.id and so on - reversing retations from course
        depth=1

# Courses
class CourseCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseCategory
        fields=['id', 'title','description','order']
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id','category','teacher', 'title','description','course_image', 'techs','related_video','tech_lists','created_date','updated_date']
#----------------------------------------------------------
class AllCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id','category','teacher', 'title','description','course_image', 'techs','course_chapters','related_video','tech_lists','created_date','updated_date']
        depth=1



# Students
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['id', 'user', 'interested_categories','created_date','updated_date','profile_img']
        # depth=1

class StudentEnrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentEnrolledCourse
        fields=['id', 'student', 'course','enrolled_date']
        depth=1
    # def __init__(self, *args, **kwargs):
    #     super(StudentEnrolledCourse,self).__init__( *args, **kwargs)
    #     request = self.context.get('request') 
    #     self.Meta.depth=0
    #     if request and request.method=='GET':
    #         self.Meta.depth=2

class CourseRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model=CourseRating
        fields=['id', 'student', 'course', 'rating', 'reviews', 'reviewed_date']
        depth=1
    # def __init__(self, *args, **kwargs):
    #     super(CourseRating,self).__init__( *args, **kwargs)
    #     request = self.context.get('request') 
    #     self.Meta.depth=0
    #     if request and request.method=='GET':
    #         self.Meta.depth=2
# ----------- Chaper --------------
class ChapterCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=ChapterCategory
        fields=['id', 'title', 'created_date']

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model=Chapter
        fields=['id','course', 'title','category','description','html', 'remarks','created_date','updated_date']
        depth=1
    # def __init__(self, instance=None, data=..., **kwargs):
    #     print('ChapterSerializer().__init__')
    #     super().__init__(instance, data, **kwargs)
    #     request = self.context.get('request') 
    #     self.Meta.depth=0
    #     if request and request.method=='GET':
    #         self.Meta.depth=1