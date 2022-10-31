from rest_framework import serializers
from api.models import *
from django.db import IntegrityError
from django.core.exceptions import ValidationError

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
        fields=['id','category','teacher', 'title','description','course_image', 'course_views' ,'taken','created_date','updated_date']
        
#----------------------------------------------------------
class AllCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=Course
        fields=['id','category','teacher', 'title','description','course_image','course_views' ,'taken','created_date','updated_date']
        depth=1



# Students
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields=['id', 'user','team', 'created_date','updated_date','profile_img']
        depth=1

class StudentEnrolledCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model=StudentEnrolledCourse
        fields=['id', 'student', 'course','enrolled_date']
        # depth=1
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

class ChapterContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=ChapterContent
        fields=['id', 'chapter_category','title','creater','file', 'url','text','content_no','created_date']

class ChapterSerializer(serializers.ModelSerializer):#'file','url', 'text',
    content = ChapterContentSerializer(read_only = True, many = True)
    class Meta:
        model=Chapter
        fields=['id','content','course', 'title','sub_title','description','chapter_no','created_date','updated_date']
        # depth=1
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(str(e))
    
class ChapterViewedSerializer(serializers.ModelSerializer):#'file','url', 'text',
    content = ChapterContentSerializer(read_only = True, many = True)
    viewed = serializers.SerializerMethodField(method_name='get_viewed')
    class Meta:
        model=Chapter
        fields=['id','content','viewed','course', 'title','sub_title','description','chapter_no','created_date','updated_date']
        # depth=1
    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError as e:
            raise serializers.ValidationError(str(e))
    # def __init__(self, *args, **kwargs):
    #         super().__init__(*args, **kwargs)
    #         if self.context.get('user_id'):
    #             # Do something
    #             print('no user_id')
    #             pass
           

    def get_viewed(self, chapterObj):
        # print(self.context.get('user_id'))
        user_id = self.context['user_id']
        
        
        try:
            viewed_count = Student.objects.filter(student_chapter_contentViewed__student__id=user_id, 
                    student_chapter_contentViewed__chapter__id=chapterObj.id,
                    student_chapter_contentViewed__viewed=True
                    ).count()
            print('--get_viewed: userid', user_id,', chapterid', ', chapter_title',chapterObj.title, chapterObj.id, 'viewed-count: ', viewed_count)
            return viewed_count
        except:
            return 0

    # def __init__(self, instance=None, data=..., **kwargs):
    #     print('ChapterSerializer().__init__')
    #     super().__init__(instance, data, **kwargs)
    #     request = self.context.get('request') 
    #     self.Meta.depth=0
    #     if request and request.method=='GET':
    #         self.Meta.depth=1