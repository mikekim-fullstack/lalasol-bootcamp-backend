from ast import If
import re
from time import time


from account.models import UserRole
from account.models import UserAccount
from api.models import *
from api.serializers import *
from rest_framework import generics
from rest_framework import permissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import json
from django.utils import timezone


class TeacherListsView(generics.ListCreateAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes=[permissions.IsAuthenticated]

class TeacherDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    # permission_classes=[permissions.IsAuthenticated]



class CourseCategoryListsView(generics.ListCreateAPIView):
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()
    # permission_classes=[permissions.IsAuthenticated]

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes=[permissions.IsAuthenticated]

class AllCourseListsView(generics.ListAPIView):
    serializer_class = AllCourseSerializer
    # queryset = Course.objects.all().order_by('-id')
    print('---- CourseListsView----')
    def get_param_from_request(self, string_param):
        '''
            First search in query_params and if not in there then search in kwargs array
            and return the result.
        '''
        param=self.request.query_params.get(string_param,None)
        if not param and string_param in self.kwargs:
                param = self.kwargs[string_param]
                print('param: ', param)
        return param
    def get_queryset(self):
        result=''
        qs=None
        if(self.request.method=='GET'):
            # self.request.query_params or self.request.GET contains by .../?query_key=query_value
            # sel.kwargs contains by .../keyword_value
            # self.request.GET has both cases.

            print('query_params: ', self.request.query_params,'kwargs:  ', self.kwargs,'', 'GET: ',self.request.GET)
            # print('request.GET: ', self. )
            limit = self.get_param_from_request('limit')
            category_slug = self.get_param_from_request('category_slug')
            skill_name = self.get_param_from_request('skill_name')
            teacher_id = self.get_param_from_request('teacher_id')
            student_id = self.get_param_from_request('student_id')
            search = self.get_param_from_request('search')

            print('skill_name', skill_name , teacher_id)

            if(limit):
                '''
                    Find the latest updated courses by limit.
                '''
                try:
                    qs = Course.objects.all().order_by('-updated_date')[:int(limit)]
                    print('>>CourseListsView-limit: ',  limit )
                except:
                    print('>>CourseListsView: ',  "no match" )
            elif(category_slug):
                '''
                    Find all courses where category_slug matches to the course's techs.
                '''
                try:
                    qs = Course.objects.filter(techs__icontains=category_slug)
                    print('>>CourseListsView-category_slug: ',  category_slug )
                except:
                    print('>>CourseListsView: ',  "no match" )
            elif(skill_name and teacher_id):
                '''
                    Find all courses where skill_name matches to course's techs by teacher_id.
                '''
                print('== skill_name, teacher_id', skill_name, teacher_id)
                try:
                    qs=Course.objects.filter(techs__icontains=skill_name, teacher=int(teacher_id))
                except:
                    print('>>CourseListsView: ',  "no match" )
                    # qs=Course.objects.all()
            elif(student_id):
                '''
                    Find all courses where the student's interested_categories matches to course's techs by student_id.
                '''
                try:
                    student_id=int(student_id)
                    student = Student.objects.get(id=student_id)
                    if(student):
                        # -- Regular expression( '\s|,' ) meaning that find the space to end of line or comma
                        # and split by them and choose only not empty string from the splited array.
                        queries_string=[Q(techs__iendswith=c) for c in re.split(r'\s|,',student.interested_categories.strip()) if c]
                        # -- queries are joined with AND so switch it to OR
                        queries = queries_string.pop()
                        for item in queries_string:
                            queries |=item
                        print('stuent: ', queries)

                        return Course.objects.filter(queries)
                except:
                    print('interested_categories does not match with techs in cousrs')
            elif search :
                '''
                    Find all couses whrere search_string is in title or techs fields
                '''
                try:
                    return Course.objects.filter(Q(title__icontains=search)|Q(techs__icontains=search))
                except:
                    print('search query has an error')
            else:
                print('no matches: ')
                qs = Course.objects.all()
        return qs



class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = AllCourseSerializer

class CourseUpdateView(generics.UpdateAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class CourseDeleteView(generics.DestroyAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    # permission_classes=[permissions.IsAuthenticated]

class ChapterListsView(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer
    # queryset = Chapter.objects.all()
    # permission_classes=[permissions.IsAuthenticated]
    # @csrf_exempt
    # @xframe_options_exempt
    def get_queryset(self):
        return Chapter.objects.all()


class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    # permission_classes=[permissions.IsAuthenticated]
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['chapter_duration'] = self.chapter_duration
    #     print('context----->', context)
    #     return context


class CourseChapterListsView(generics.ListAPIView):
    serializer_class = ChapterSerializer
    # permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        course_id = self.kwargs['course_id']
        print('course_id: ', course_id)
        # course = Course.objects.get(id=course_id)
        # chapter = Chapter.objects.filter(course=course)
        chapter = Chapter.objects.filter(course=course_id)
        return chapter

class TeacherCourseListsView(generics.ListAPIView):
    serializer_class = CourseSerializer
    def get_queryset(self):
        teacher_id = self.kwargs['teacher_id']
        teacher = Teacher.objects.get(id=teacher_id)
        # self.queryset = Course.objects.filter(teacher=teacher)
        return Course.objects.filter(teacher=teacher)
    # permission_classes=[permissions.IsAuthenticated]


#---------------- Student -------------------------
@csrf_exempt # stop Cross-Site Reqeust Forgery  protection
def StudentLogin(request):
    # print('student login request: ', request.body, request.method)
    if request.method=='POST':
        # print('request.body.decode): ', request.body.decode('utf-8'))
        data = json.loads(request.body.decode('utf-8'))#Json object to python object
        # data = request.body.decode('utf-8')#Json object to python object
        # print('student email: ', data['email'])
        email = data['email']
        password = data['password']
        if(email and password):
            print('studen email password: ', email, password)
            # return JsonResponse({'bool':True,'email':email, 'password':password}) #test
            try:
                # -- Get Student RoleType: 0. --
                role = UserRole.objects.get(role_type=0)
                user=UserAccount.objects.get(email=email, password=password, role=role)
                user.last_login=timezone.now()
                user.save()
                # # -- check if user is a student. --
                # isStudent = False
                # for i in user.role.all():
                #     if i.get_mytype()=='STUDENT':isStudent=True
                # if not isStudent: return JsonResponse({'bool':False,'error':'Your aren\'t a student!'})
                try:
                    student = Student.objects.get(user=user)
                    print('user: ', user.role.all(), str(user.email), student.team , student.profile_img)
                except(Student.DoesNotExist, Student.MultipleObjectsReturned) as e:
                    return JsonResponse({'bool':False, 'error':str(e)})
            except(UserAccount.DoesNotExist, UserAccount.MultipleObjectsReturned) as e:
            # except :
                print('error----', e)
                return JsonResponse({'bool':False, 'error':str(e)})
            finally:
                print('final student login----')
            if student:
                return JsonResponse({'bool':True,'id':user.id,', email': user.email, 'full_name':user.get_full_name()})
                # return JsonResponse({'bool':True,'id':user.id, 'full_name':studentData.full_name})
            else:
                return JsonResponse({'bool':False,'error':'User does not exist'})
        else:
            return JsonResponse({'bool':False, 'error':'email or password is missing'})
    else:
        return JsonResponse({'boo':'fasle','error': 'wrong request'})

# ---------- StudentSignUp ----------
#  --- reqest: form-data input so use request.POST and request.FILES. ---
@csrf_exempt # stop Cross-Site Reqeust Forgery  protection
def StudentSignUp(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        imageUrl = request.FILES.get('image')
        myteam = request.POST.get('team')
        # print('---',email, password, firstName, lastName, imageUrl, myteam)
        if email and password and firstName and lastName :
            # --- Get Role Object for Student. ---
            try:
                role = UserRole.objects.get(role_type=0)
            except:
                return JsonResponse({'bool':False, 'error': 'Student Role does not exist!'})

            # --- Check if UserAccount Object exists or not. ---
            user = UserAccount.objects.filter(email=email, 
                    first_name=firstName,
                    last_name=lastName,
                    role=role, 
                    ).exists()
            if(user):
                return JsonResponse({'bool':False, 'error': 'User '+email+' already exist!'})
                
            # --- Get team object. ---
            if(myteam):
                try:
                    team = Team.objects.get(name=myteam)
                except(Team.DoesNotExist) as e:
                    team=None
            
            print(team, imageUrl)

            # --- Create new UserAccount object. ---
            try:
                newUser = UserAccount.objects.create(email=email, 
                    password=password, 
                    first_name=firstName,
                    last_name=lastName,
                    
                    )
                newUser.role.add(role)
                newUser.save()
                # --- Create new Student object. ---
                try:
                   newStudent = Student.objects.create(user=newUser)
                   if(team): newStudent.team = team
                   if(imageUrl): newStudent.profile_img = imageUrl
                   newStudent.save()
                except:
                    newUser.delete()
                    # print('error-newUser Creation')
                    return JsonResponse({'bool':False, 'error':'Fail to create Student'})
            except:
                # print('---error---')
                return JsonResponse({'bool':False, 'error':'Fail to create Student'})
        return JsonResponse({'bool':True, 'message':'Student successfully created!'})

        
class StudentListsView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # def get_queryset(self):
    #     print('StudentListsView')
    #     return super().get_queryset()
    # permission_classes=[permissions.IsAuthenticated]
    # def get_queryset(self):
    #     usrRole= UserRole.objects.filter(role_type=1).values()[0]
    #     # usr = UserAccount.objects.filter(user=usrRole).distinct('id')
    #     role = Student.objects.filter(role__id=1)
    #     print('usr=',role, ', role=',usrRole)
    #     student=Student.objects.all()#Student.objects.filter(user=usr).distinct('id')
    #     # print('-----',student)
    #     if(student):
    #             return student
    #     else:
    #             return student

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    # permission_classes=[permissions.IsAuthenticated]

class StudentCourseEnrollmentLists(generics.ListCreateAPIView):
    queryset = StudentEnrolledCourse.objects.all()
    serializer_class=StudentEnrolledCourseSerializer
    # def get_queryset(self):
    #     print('StudentCourseEnrollmentLists', super().get_queryset())
    #     return super().get_queryset()

def fetch_enroll_status(request, course_id, student_id):
    enroll = StudentEnrolledCourse.objects.get(course=course_id, student=student_id)
    if enroll:
        return JsonResponse({'bool':'true'})
    
    return JsonResponse({'bool':'false'})

class EnrolledStudentLists(generics.ListAPIView):
    serializer_class=StudentEnrolledCourseSerializer
    def get_queryset(self):
        print('-----',self.kwargs,', data:', self.request.GET.get('course_id'),self.request.GET.get('teacer_id'))
        course_id = self.request.GET.get('course_id')
        teacher_id = self.request.GET.get('teacher_id')
        if course_id:#'course_id' in self.kwargs:
            # course_id = self.kwargs['course_id']
            course=StudentEnrolledCourse.objects.filter(course=course_id).distinct('id')
            if(course):
                return course
            else:
                return None
        elif teacher_id:#'teacher_id' in self.kwargs:
            # teacher_id = self.kwargs['teacher_id']
            teacher=StudentEnrolledCourse.objects.filter(course__teacher=teacher_id)
            print('teacher_id: ', teacher)
            
            if(teacher):
                return teacher
            else:
                return None
        
        return StudentEnrolledCourse.objects.all()

class CourseRatingLists(generics.ListCreateAPIView):
    serializer_class=CourseRatingSerializer
    def get_queryset(self):
        # if 'course_id' in self.kwargs:
        #     course_id = self.kwargs['course_id']
        #     if course_id:
        #         return CourseRating.objects.filter(course=course_id)
        if 'popular' in self.request.GET:
            sql='SELECT *, AVG(cr.rating) as avg_rating FROM api_courserating as cr \
                INNER JOIN api_course as c ON cr.course_id=c.id \
                GROUP BY c.id ORDER BY avg_rating decs LIMIT 4;'
            return CourseRating.objectS.raw(sql)
        if 'all' in self.request.GET:
            sql='SELECT *, AVG(cr.rating) as avg_rating FROM api_courserating as cr \
                INNER JOIN api_course as c ON cr.course_id=c.id \
                GROUP BY c.id ORDER BY avg_rating decs;'
            return CourseRating.objectS.raw(sql)
        return CourseRating.objects.all()

def fetch_rating_status(request, student_id, course_id):
    count = CourseRating.objects.filter(student=student_id, course=course_id).count()
    if(count>0):
        return JsonResponse({'bool':'true'})
    return JsonResponse({'bool':'false'})
