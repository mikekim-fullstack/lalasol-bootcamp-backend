from cmath import exp
from email.policy import HTTP
from http import HTTPStatus
from numbers import Number
import re
from time import time
import json
from unicodedata import category
from django.utils import timezone

from account.models import UserRole
from account.models import UserAccount
from api.models import *
from api.serializers import *
from rest_framework import generics
from rest_framework import permissions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.views.decorators.clickjacking import xframe_options_exempt





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

class CourseCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CourseCategorySerializer
    queryset = CourseCategory.objects.all()
    # permission_classes=[permissions.IsAuthenticated]

class CourseCreateView(generics.CreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # permission_classes=[permissions.IsAuthenticated]

class AllCourseListsView(generics.ListAPIView):
    serializer_class = AllCourseSerializer
    queryset = Course.objects.all().order_by('-id')
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
    # def get_queryset(self):
    #     result=''
    #     qs=None
    #     if(self.request.method=='GET'):
    #         # self.request.query_params or self.request.GET contains by .../?query_key=query_value
    #         # sel.kwargs contains by .../keyword_value
    #         # self.request.GET has both cases.

    #         print('query_params: ', self.request.query_params,'kwargs:  ', self.kwargs,'', 'GET: ',self.request.GET)
    #         # print('request.GET: ', self. )
    #         limit = self.get_param_from_request('limit')
    #         category_slug = self.get_param_from_request('category_slug')
    #         skill_name = self.get_param_from_request('skill_name')
    #         teacher_id = self.get_param_from_request('teacher_id')
    #         student_id = self.get_param_from_request('student_id')
    #         search = self.get_param_from_request('search')

    #         print('skill_name', skill_name , teacher_id)

    #         if(limit):
    #             '''
    #                 Find the latest updated courses by limit.
    #             '''
    #             try:
    #                 qs = Course.objects.all().order_by('-updated_date')[:int(limit)]
    #                 print('>>CourseListsView-limit: ',  limit )
    #             except:
    #                 print('>>CourseListsView: ',  "no match" )
    #         elif(category_slug):
    #             '''
    #                 Find all courses where category_slug matches to the course's techs.
    #             '''
    #             try:
    #                 qs = Course.objects.filter(techs__icontains=category_slug)
    #                 print('>>CourseListsView-category_slug: ',  category_slug )
    #             except:
    #                 print('>>CourseListsView: ',  "no match" )
    #         elif(skill_name and teacher_id):
    #             '''
    #                 Find all courses where skill_name matches to course's techs by teacher_id.
    #             '''
    #             print('== skill_name, teacher_id', skill_name, teacher_id)
    #             try:
    #                 qs=Course.objects.filter(techs__icontains=skill_name, teacher=int(teacher_id))
    #             except:
    #                 print('>>CourseListsView: ',  "no match" )
    #                 # qs=Course.objects.all()
    #         elif(student_id):
    #             '''
    #                 Find all courses where the student's interested_categories matches to course's techs by student_id.
    #             '''
    #             try:
    #                 student_id=int(student_id)
    #                 student = Student.objects.get(id=student_id)
    #                 if(student):
    #                     # -- Regular expression( '\s|,' ) meaning that find the space to end of line or comma
    #                     # and split by them and choose only not empty string from the splited array.
    #                     queries_string=[Q(techs__iendswith=c) for c in re.split(r'\s|,',student.interested_categories.strip()) if c]
    #                     # -- queries are joined with AND so switch it to OR
    #                     queries = queries_string.pop()
    #                     for item in queries_string:
    #                         queries |=item
    #                     print('stuent: ', queries)

    #                     return Course.objects.filter(queries)
    #             except:
    #                 print('interested_categories does not match with techs in cousrs')
    #         elif search :
    #             '''
    #                 Find all couses whrere search_string is in title or techs fields
    #             '''
    #             try:
    #                 return Course.objects.filter(Q(title__icontains=search)|Q(techs__icontains=search))
    #             except:
    #                 print('search query has an error')
    #         else:
    #             print('no matches: ')
    #             qs = Course.objects.all()
    #     return qs
        



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

class ChapterConentListsView(generics.ListCreateAPIView):
    serializer_class = ChapterContentSerializer 
    queryset = ChapterContent.objects.all()



class ChapterListsView(generics.ListCreateAPIView):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    '''
    def post(self, request, *args, **kwargs):
        course_id = request.data.get('course')
        name = request.data.get('name')
        # chapter_no = request.data.get('chapter_no')
        description = request.data.get('description')
        chapterObject=None
        if(course_id and name   and description):
            try:
                course = Course.objects.get(id=course_id)
                chapterObject = Chapter.objects.create(
                    course=course,
                    name=name,
                    # chapter_no=int(chapter_no),
                    description=description
                    )
            except:
                return JsonResponse({'bool':False, 'error':'one of input missing'}, status=HTTPStatus.BAD_REQUEST)
            pass
        else :
            return JsonResponse({'bool':False, 'error':'one of input missing'}, status=HTTPStatus.BAD_REQUEST)
        
        # Parsing reqest dat for the nested content data and store in cotent array like this.
        # e.g. Input: content[0].chapter_category
        #             content[0].creater
        #             content[0].content_no
        #      Output in cotent array
        #     [
        #         {'file': <InMemoryUploadedFile: html-css-homework-1.html (text/html)>, 'chapter_category': 1, 'creater': 1, 'content_no': 2}, 
        #         {'file': <InMemoryUploadedFile: html-css-practice-1.html (text/html)>, 'chapter_category': 1, 'creater': 1, 'content_no': 3}
        #     ]
        
        content=[]
        for key in request.data:
            if(key.startswith('content')):
                # -- Search for [number] and get number
                m = int(re.search(r"\[([0-9]+)\]", key).group(1))
                # get last word
                pattern = re.compile(r"(\w+)$")
                has = pattern.search(key).group(0)       

                size = m-len(content)+1
                # -- if necessary, create dictionary and append it into array.
                if(size>0):
                    for i in range(size):
                        # print('i: ', i)
                        content.append({'type':'','file':'', 'url':'','text':'','chapter_category':0, 'creater':0, 'content_no':0})
                if has=='file':
                    content[m]['file'] = request.data.get(key)
                    content[m]['type'] = 'file'
                elif has=='url':
                    content[m]['url'] = request.data.get(key)
                    content[m]['type'] = 'url'
                elif has=='text':
                    content[m]['text'] = request.data.get(key)
                    content[m]['type'] = 'text'
                elif has=='chapter_category':
                    content[m]['chapter_category'] = int(request.data.get(key))
                elif has=='content_no':
                    content[m]['content_no'] = int(request.data.get(key))
                elif has=='creater':
                    content[m]['creater'] = int(request.data.get(key))
                else :
                    print('--- raise error ---')
                    pass
                # print (m, has,request.data.get(key))
                # print(key)
        # print('----------------',content, len(content),'--------------/n')#,' ,',{'a':request.data.get('content[1].file')}, request.data.get('content[1].file'))
        content_id=[]
        for item in content:
            # print(item['file'],item['chapter_category'],item['creater'],item['content_no'])
            try:
                chapter_category = ChapterCategory.objects.get(id=item['chapter_category'])
                creater = Teacher.objects.get(id=item['creater'])
                # print('chapter_category----',item['chapter_category'], chapter_category)
                
                # validated_data = ChapterContentSerializer(
                #         chapter_category=chapter_category.id,
                #     creater=creater.id,
                #     content_no=item['content_no'],
                #     file=item['file']
                # )

                new_content = ChapterContent.objects.create(
                    chapter_category=chapter_category,
                    creater=creater,
                    content_no=item['content_no'],
                    file=item['file'],
                    url=item['url'],
                    text=item['text']
                )
                content_id.append(new_content.id)
            
            except:
                if(type(chapterObject)!=None):
                    qs = Chapter.objects.filter(pk=chapterObject.id)
                    # print('type', type(chapterObject),chapterObject.id, ', qs:',qs,' end')
                    qs.delete()
                return JsonResponse({'bool':False, 'error':'Faied to create chapter'}, status=HTTPStatus.BAD_REQUEST)

                # print('error-validation', type(chapterObject),  chapterObject)
        ## -- Finally add all content to chapter
        for contentId in content_id:
            try:
                chapterObject.content.add(contentId)
            except:
                return JsonResponse({'bool':False, 'error':'adding conent failed'}, status=HTTPStatus.NO_CONTENT)

       
        return JsonResponse({'bool':True}, status=HTTPStatus.CREATED)
    '''
   
    # def post(self, request, format=None):
    #     print('---------ChapterListsView: ', request.data)
    #     query = request.data.get('query')
    # permission_classes=[permissions.IsAuthenticated]
    # @csrf_exempt
    # @xframe_options_exempt
    # def get_queryset(self):
    #     return Chapter.objects.all()


class ChapterUpdateView(generics.UpdateAPIView):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    def put(self, request, *args, **kwargs):
        print(request.data)
        chapter_id = request.data.get('chapter_id')
        name = request.data.get('name')
        # chapter_no = request.data.get('chapter_no')
        description = request.data.get('description')

        

        if(not chapter_id or not name  or not description):
            return JsonResponse({'bool':False, 'error':'input is missing'}, status=HTTPStatus.NOT_FOUND)
        # -- Get Content data. --
        content=[]
        for key in request.data:
            if(key.startswith('content')):
                # -- Search for [number] and get number
                m = int(re.search(r"\[([0-9]+)\]", key).group(1))
                # get last word
                pattern = re.compile(r"(\w+)$")
                has = pattern.search(key).group(0)       

                size = m-len(content)+1
                # -- if necessary, create dictionary and append it into array.
                if(size>0):
                    content.append({'id':0,'file':'', 'url':'','text':'','chapter_category':0, 'creater':0, 'content_no':0})
                if has=='file':
                    content[m]['file'] = request.data.get(key)
                    
                elif has=='url':
                    content[m]['url'] = request.data.get(key)
                    
                elif has=='text':
                    content[m]['text'] = request.data.get(key)
                   
                elif has=='chapter_category':
                    content[m]['chapter_category'] = int(request.data.get(key))
                elif has=='content_no':
                    content[m]['content_no'] = int(request.data.get(key))
                elif has=='creater':
                    content[m]['creater'] = int(request.data.get(key))
                elif has=='id':
                    content[m]['id'] = int(request.data.get(key))
                else :
                    print('--- raise error ---')
                    pass
        print('/n ------ content: ', content,'\n\n')
        #------------------------------------------------------------
        try:
            chapter = Chapter.objects.get(id=chapter_id)

            
            chapter.name = name
            # chapter.sub_title = sub_title
            # chapter.chapter_no = chapter_no
            chapter.description = description
            chapter.save()

            for itemConent in content:
                # contentObj = ChapterContent.objects.filter(chapter__id=chapter_id).order_by('id')
                try:
                    contentObj = ChapterContent.objects.filter(id=itemConent['id'])
                    print('chapter', chapter, contentObj,', file: ',itemConent['file'], itemConent['id'])
                    if(len(contentObj)>0 and contentObj[0]):
                        contentObj = contentObj[0]
                        contentObj.delete()
                        try:
                            chapter_category = ChapterCategory.objects.get(id=itemConent['chapter_category'])
                            creater = Teacher.objects.get(id=itemConent['creater'])
                            new_content = ChapterContent.objects.create(
                                chapter_category=chapter_category,
                                creater=creater,
                                content_no=itemConent['content_no'],
                                file=itemConent['file'],
                                url=itemConent['url'],
                                text=itemConent['text']
                                )
                            chapter.content.add(new_content)
                            chapter.save()

                            print('created_content: ', new_content)
                        except:
                            return JsonResponse({'bool':False, 'error':'Faied to update content'}, status=HTTPStatus.BAD_REQUEST)
                            # print('**failed to create content**', itemConent['chapter_category'],
                            # itemConent['creater'],
                            # itemConent['content_no'],
                            # itemConent['file'],
                            # itemConent['url'],
                            # itemConent['text']
                            # )
 
                    #     if( (itemConent['url']!='' or itemConent['text']!='' or itemConent['file']!='' ) and contentObj.file !='' ):
                    #         contentObj.delete()
                    #         try:
                    #             chapter_category = ChapterCategory.objects.get(id=itemConent['chapter_category'])
                    #             creater = Teacher.objects.get(id=itemConent['creater'])
                    #             new_content = ChapterContent.objects.create(
                    #                 chapter_category=chapter_category,
                    #                 creater=creater,
                    #                 content_no=itemConent['content_no'],
                    #                 file=itemConent['file'],
                    #                 url=itemConent['url'],
                    #                 text=itemConent['text']
                    #                 )
                    #             chapter.content.add(new_content)
                    #             chapter.save()

                    #             print('created_content: ', new_content)
                    #         except:
                    #             return JsonResponse({'bool':False, 'error':'Faied to update content'}, status=HTTPStatus.BAD_REQUEST)
                    #             # print('**failed to create content**', itemConent['chapter_category'],
                    #             # itemConent['creater'],
                    #             # itemConent['content_no'],
                    #             # itemConent['file'],
                    #             # itemConent['url'],
                    #             # itemConent['text']
                    #             # )
                            
                    # else:
                    #     contentObj.update(chapter_category = itemConent['chapter_category'])
                    #     contentObj.update(content_no = itemConent['content_no'])
                    #     contentObj.update(creater = itemConent['creater'])
                    #     contentObj.update(url = itemConent['url'])
                    #     contentObj.update(text = itemConent['text'])  
                except:
                    return JsonResponse({'bool':False, 'error':'Faied to update content'}, status=HTTPStatus.BAD_REQUEST)
            # print('chapter.content: ', chapter.objects.filter(content__id=29))
        except:
            return JsonResponse({'bool':False, 'error':'Faied to find chapter'}, status=HTTPStatus.BAD_REQUEST)

        return JsonResponse({'bool':True}, status=HTTPStatus.OK)
        pass

@csrf_exempt
def create_chapter_content(request):
    pass
class ChapterCategoryListsView(generics.ListCreateAPIView):
    serializer_class = ChapterCategorySerializer
    queryset = ChapterCategory.objects.all()

@csrf_exempt
def set_chapter_content_viewed(request):
    if(request.method=='POST'):
        student_id = request.POST.get('student_id')
        chapter_id = request.POST.get('chapter_id')
        content_id = request.POST.get('content_id')
        print('set_chapter_content_viewed: ', student_id,chapter_id,content_id  )
        if(content_id and chapter_id and student_id):
            try:
                qs = StudentChapterContentViewed.objects.get(student=student_id,chapter=chapter_id, content=content_id)
                print('set_chapter_content_viewed---updated', qs)
                if not qs.viewed:
                    qs.viewed=True
                qs.viewed_date=timezone.now()
                qs.save()
                
                return JsonResponse({'bool':True,'message':'successfully updated' })
            except StudentChapterContentViewed.DoesNotExist:
                try:
                    # StudentChapterContentViewed.objects.filter(student=student_id, content=content_id, chapter=chapter_id).delete()
                    
                    student = Student.objects.get(id=student_id)
                    chapter = Chapter.objects.get(id=chapter_id)
                    content = ChapterContent.objects.get(id=content_id)
                    StudentChapterContentViewed.objects.create(student=student, chapter=chapter, content=content, viewed=True)
                    print('set_chapter_content_viewed---created')
                    return JsonResponse({'bool':True,'message':'successfully created' })
                except (Student.DoesNotExist, Chapter.DoesNotExist,ChapterContent.DoesNotExist ) as e:
                    return JsonResponse({'bool':False, 'error':str(e)}, status=HTTPStatus.NOT_FOUND)
        else:
            return JsonResponse({'bool':False, 'error':'one of input missing'}, status=HTTPStatus.BAD_REQUEST)
    return JsonResponse({'bool':False, 'error':'request is wrong!'}, status=HTTPStatus.BAD_REQUEST)


@csrf_exempt
def get_chapter_viewed(request):
    if(request.method=='GET'):
        student_id = request.GET.get('student_id')
        chapter_id = request.GET.get('chapter_id')
        print('-- get_chapter_viewed: ', student_id, chapter_id)
        if(chapter_id and student_id):
            try:
                qs_content_viewed = Student.objects.filter(student_chapter_contentViewed__student__id=student_id, 
                student_chapter_contentViewed__chapter__id=chapter_id,
                student_chapter_contentViewed__viewed=True
                )

                chapter_total_content = Chapter.objects.get(id=chapter_id).content.count()
                
                print('get_chapter_viewed: ', qs_content_viewed, qs_content_viewed.count(),', chapter_total_content: ',chapter_total_content)
                return JsonResponse({'bool':True,'chapter_total_content':str(chapter_total_content),'viewed_count':str(qs_content_viewed.count()) })
            except (Student.DoesNotExist, 
                    Chapter.DoesNotExist,
                    StudentChapterContentViewed.DoesNotExist) as e:
                return JsonResponse({'bool':False, 'error':str(e)}, status=HTTPStatus.NOT_FOUND)
        else:
            return JsonResponse({'bool':False, 'error':'one of input missing'}, status=HTTPStatus.BAD_REQUEST)
        
    return JsonResponse({'bool':False, 'error':'request is wrong!'}, status=HTTPStatus.BAD_REQUEST)

class ChapterDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ChapterSerializer
    queryset = Chapter.objects.all()
    # lookup_url_kwarg = 'user_id'
    # print('lookup_url_kwarg: ', lookup_url_kwarg)

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
        try:
            print('request.body): ',request.body, request.body.decode('utf-8'))
            # print('request.body.decode): ', request.body.decode('utf-8'))
            data = json.loads(request.body.decode('utf-8'))#Json object to python object
        except:
            return JsonResponse({'bool':False, 'error':'No input'}, status=HTTPStatus.BAD_REQUEST)
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
                    return JsonResponse({'bool':False, 'error':str(e)}, status=HTTPStatus.BAD_REQUEST)
            except(UserAccount.DoesNotExist, UserAccount.MultipleObjectsReturned) as e:
            # except :
                print('error----', e)
                return JsonResponse({'bool':False, 'error':str(e)},status=HTTPStatus.BAD_REQUEST)
            finally:
                print('final student login----')
            if student:
                return JsonResponse({'bool':True,'id':student.id,'email': user.email, 'first_name':user.first_name, 'last_name':user.last_name, 'role':'student'})
                # serializer = StudentSerializer(student)
                # print('---output----' , student, json.dumps(serializer.data))
                # return JsonResponse(serializer.data)
            else:
                return JsonResponse({'bool':False,'error':'User does not exist'}, status=HTTPStatus.BAD_REQUEST)
        else:
            return JsonResponse({'bool':False, 'error':'email or password is missing'}, status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse({'boo':'fasle','error': 'wrong request'}, status=HTTPStatus.BAD_REQUEST)

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
        else:
            return JsonResponse({'bool':False, 'message':'One of information missing!'})

        
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
@csrf_exempt
def manage_student_enroll_course(request, student_id, cat_id):
    try:
        student = Student.objects.get(id = student_id)
        allCourse = Course.objects.filter(category_id = cat_id)
        print('student: ', student, ' ,allCourse: ',allCourse)
        # StudentEnrolledCourse.objects.create(student=1,course=5)
        if allCourse.exists():
            for course in allCourse.iterator():
                
                if(not StudentEnrolledCourse.objects.filter(student__id=student.id,course__id=course.id).exists()):
                    print('StudentEnrolledCourse is created: ', student, course, course.id)
                    StudentEnrolledCourse.objects.create(student=student,course=course)
                    
            return JsonResponse({'bool':'true'})
        else:
            return JsonResponse({'bool':'false','message':'no data'})
    except:
        return JsonResponse({'bool':'false'})
    
   
    

@csrf_exempt
def fetch_viewed_chapters_by_course_id(request):
    try:
        if(request.method=='GET'):
            user_id = request.GET.get('user_id')
            course_id = request.GET.get('course_id')
            # print('fetch_chapters_by_course_id: ', user_id, course_id)
            if(user_id and course_id ):
                chapters = Chapter.objects.filter(course__id=course_id)
                try:
                    # serializer  = ChapterSerializer(chapters, many=True)
                    serializer  = ChapterViewedSerializer(chapters, many=True, context={'user_id': user_id})
                    # print('chapter: ', serializer_c,(serializer.data))
                    return JsonResponse(serializer.data, safe=False)
                except:
                    return JsonResponse({'bool':'false'}, status=HTTPStatus.NOT_FOUND)
            else:
                return JsonResponse({'bool':'false'}, status=HTTPStatus.NOT_FOUND)
        else:
            return JsonResponse({'bool':'false'}, status=HTTPStatus.BAD_REQUEST)

    except:
        return JsonResponse({'bool':'false'}, status=HTTPStatus.BAD_REQUEST)
    pass
def fetch_enroll_status(request, course_id, student_id):
    enroll = StudentEnrolledCourse.objects.get(course=course_id, student=student_id)
    if enroll:
        return JsonResponse({'bool':'true'})
    
    return JsonResponse({'bool':'false'})
@csrf_exempt
def fetch_enrolled_courses_by_student_id(request, student_id):
    if(request.method=='GET'):
        course = Course.objects.filter(course_enrolled_course__student=student_id)
        print('course: ', student_id, course)
        if course:
            serializer  = CourseSerializer(course, many=True)
            # serializer  = CourseSerializer(course, many=True, context={'user_id':1})
            return JsonResponse(serializer.data, safe=False)
        
        return JsonResponse({'bool':'false'}, status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse({'bool':'false'}, status=HTTPStatus.BAD_REQUEST)
@csrf_exempt
def fetch_courses_with_enrolled_student_id(request, student_id):
    if(request.method=='GET'):
        course = Course.objects.all()
        # print('course: ', student_id, course)
        if course:
            serializer  = AllCourseEnrolledSerializer(course, many=True, context={'student_id':student_id})
            # serializer  = CourseSerializer(course, many=True, context={'user_id':1})
            return JsonResponse(serializer.data, safe=False)
        
        return JsonResponse({'bool':'false'}, status=HTTPStatus.BAD_REQUEST)
    else:
        return JsonResponse({'bool':'false'}, status=HTTPStatus.BAD_REQUEST)

@csrf_exempt
def fetch_enrolled_courses_by_student_id_n_cat_id(request, student_id, category_id):
    print('fetch_enrolled_courses_by_student_id_n_cat_id: ', student_id, category_id)
    if(request.method=='GET'):
        try: #
            course = Course.objects.filter(course_enrolled_course__student=student_id,category__id=category_id)

            serializer  = CourseSerializer(course, many=True)
            return JsonResponse(serializer.data, safe=False)
        except(Course.DoesNotExist) as e:
            print('error:',e)
            
            return JsonResponse({'bool':'false'},status = HTTPStatus.NOT_FOUND)    
    else:
        return JsonResponse({'bool':'false'}, status=HTTPStatus.BAD_REQUEST)

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
