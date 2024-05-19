from django.shortcuts import render
from rest_framework.views import APIView
from phdTracksBackend.utils import send_response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *
from django.utils import timezone
        
class indexView(APIView):
    def get(self,request):
        try:
            return send_response(result=True, message="Welcome to the PHD Tracks API")
        except Exception as e:
            return send_response(result=False, message=str(e))


class userRegistrationView(APIView):
    
    def post(self, request):
        try:
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            department = request.data.get('department', None)
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            if first_name is not None and last_name is not None and email is not None and password is not None:
                user = User.objects.filter(email=email)
                if not user.exists():
                    new_user = User.objects.create_user(email=email, first_name=first_name,last_name=last_name, password=password, department=department)
                    return send_response(result=True, message="User created successfully")
                else:
                    return send_response(result=False, message="User with this email already exists")
            else:
                return send_response(result=False, message="Empty Fields")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

class adminRegisterationView(APIView):

    def post(self,request):
        try:
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            email = request.data.get('email', None)
            password = request.data.get('password', None)
            if first_name is not None and last_name is not None and email is not None and password is not None:
                user = User.objects.filter(email=email)
                if not user.exists():
                    new_user = User.objects.create_superuser(email=email, first_name=first_name,last_name=last_name, password=password)
                    return send_response(result=True, message="User created successfully")
                else:
                    return send_response(result=False, message="User with this email already exists")
            else:
                return send_response(result=False, message="Empty Fields")
        except Exception as e:
            return send_response(result=False,message=str(e))
        


class loginView(APIView):

    def post(self,request):
        try:
            email = request.data.get('email', None)
            password = request.data.get('password', None)

            if email is not None and password is not None:
                if not User.objects.filter(email=email).exists():
                    return send_response(result=False, message='User does not exist')
                
                user = authenticate(email=email, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        refresh = RefreshToken.for_user(user)
                        user_data = UserSerializer(user).data
                        token_data = {
                            'refresh': str(refresh),
                            'access': str(refresh.access_token),
                            'user': user_data
                        }
                        return Response(TokenSerializer(token_data).data, status=status.HTTP_200_OK)
                    else:
                        return send_response(result=False, message="User is not active, contact admin")
                else:
                    return send_response(result=False, message="Invalid credentials")

            else:
                return send_response(result=False, message="Empty Fields")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

class userView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user.is_superuser:
                users = User.objects.all()
                return send_response(result=True, data=UserSerializer(users, many=True).data)
            else:
                return send_response(result=False, message="You are not authorized to view this page")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    def get(self, request, pk):
        try:
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)

            return send_response(result=True, data=UserSerializer(user).data)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    def patch(self,request,pk):
        try:
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            # if 'profile_pic' in request.data:
            #     user.profile_pic = request.data.get('profile_pic')
            if 'designation' in request.data:
                user.designation = request.data.get('designation')
            if 'first_name' in request.data:
                user.first_name = request.data.get('first_name')
            if 'last_name' in request.data:
                user.last_name = request.data.get('last_name')
            if 'area_of_research' in request.data:
                user.area_of_research = request.data.get('area_of_research')
            if 'supervisor' in request.data:
                user.supervisor = request.data.get('supervisor')
            if 'thesis_url' in request.data:
                user.thesis_url = request.data.get('thesis_url')
            if 'status' in request.data:
                user.status = request.data.get('status')    

            user.save()
            return send_response(result=True, message="User updated successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

class examinerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            examiners = Examiner.objects.filter(is_assigned=False)
            return send_response(result=True, data=ExaminerSerializer(examiners, many=True).data)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    def patch(self,request,pk):
        try:
            if not Examiner.objects.filter(pk=pk).exists():
                return send_response(result=False, message="Examiner does not exist")
            examiner = Examiner.objects.get(pk=pk)
            if 'is_assigned' in request.data:
                examiner.is_assigned = request.data.get('is_assigned')
            examiner.save()
            return send_response(result=True, message="Examiner updated successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
class form1AView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            department = request.data.get('department', None)
            name = request.data.get('name', None)
            rollno = request.data.get('rollno', None)
            education_data = request.data.get('education', [])
            area_of_research = request.data.get('area_of_research', None)
            category_of_studentship = request.data.get('category_of_studentship', None)
            recommender_1 = request.data.get('recommender_1', None)
            recommender_2 = request.data.get('recommender_2', None)

            if not department or not name or not rollno or not education_data or not area_of_research or not category_of_studentship or not recommender_1 or not recommender_2:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form1a = Form1A.objects.create(
                user=user,
                department=department,
                name=name,
                rollno=rollno,
                area_of_research=area_of_research,
                category_of_studentship=category_of_studentship,
                recommender_1=recommender_1,
                recommender_2=recommender_2
            )

            # Create Education instances and link them to Form1A
            for ed in education_data:
                serializer = EducationSerializer(data=ed)
                if serializer.is_valid():
                    education_instance = serializer.save()
                    form1a.education.add(education_instance)
                else:
                    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return send_response(result=False, message=serializer.errors)

            form1a.save()

             # Update user's form1a_submitted field
            user.form1a_submitted = timezone.now()
            user.save()
            # return Response(Form1ASerializer(form1a).data, status=status.HTTP_201_CREATED)
            return send_response(result=True, message="Form1A created successfully")
        except Exception as e:
            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
            return send_response(result=False, message=str(e))
        
class form1BView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            department = request.data.get('department', None)
            name = request.data.get('name', None)
            rollno = request.data.get('rollno', None)
            date_of_enrolment = request.data.get('date_of_enrolment', None)
            area_of_research = request.data.get('area_of_research', None)
            category_of_studentship = request.data.get('category_of_studentship', None)
            courses = request.data.get('courses', [])

            if not department or not name or not rollno or not date_of_enrolment or not area_of_research or not category_of_studentship or not courses:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form1b = Form1B.objects.create(
                user=user,
                department=department,
                name=name,
                rollno=rollno,
                date_of_enrolment=date_of_enrolment,
                area_of_research=area_of_research,
                category_of_studentship=category_of_studentship,
            )

            # Create Education instances and link them to Form1A
            for course in courses:
                serializer = CourseSerializer(data=course)
                if serializer.is_valid():
                    course_instance = serializer.save()
                    form1b.course.add(course_instance)
                else:
                    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return send_response(result=False, message=serializer.errors)

            form1b.save()

             # Update user's form1a_submitted field
            user.form1b_submitted = timezone.now()
            user.save()
            # return Response(Form1ASerializer(form1a).data, status=status.HTTP_201_CREATED)
            return send_response(result=True, message="Form1B created successfully")
        except Exception as e:
            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
            return send_response(result=False, message=str(e))


class form2View(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            department = request.data.get('department', None)
            name = request.data.get('name', None)
            month_year = request.data.get('month_year', None)
            rollno = request.data.get('rollno', None)
            date_of_joining = request.data.get('date_of_joining', None)
            work_done = request.data.get('work_done', None)
            nature_of_work = request.data.get('nature_of_work', None)
            remarks_by_supervisor = request.data.get('remarks_by_supervisor', [])

            if not department or not name or not rollno or not date_of_joining or not work_done or not nature_of_work or not remarks_by_supervisor or not month_year:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form2 = Form2.objects.create(
                user=user,
                department=department,
                name=name,
                rollno=rollno,
                month_year=month_year,
                date_of_joining=date_of_joining,
                work_done=work_done,
                nature_of_work=nature_of_work,
            )

            # # Create Education instances and link them to Form1A
            # for course in courses:
            #     serializer = CourseSerializer(data=course)
            #     if serializer.is_valid():
            #         course_instance = serializer.save()
            #         form2.course.add(course_instance)
            #     else:
            #         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #         return send_response(result=False, message=serializer.errors)

            form2.save()

             # Update user's form1a_submitted field
            user.form2_submitted = timezone.now()
            user.save()
            # return Response(Form1ASerializer(form1a).data, status=status.HTTP_201_CREATED)
            return send_response(result=True, message="Form2 created successfully")
        except Exception as e:
            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
            return send_response(result=False, message=str(e))
        
class form3AView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            name = request.data.get('name', None)
            seminar_date = request.data.get('seminar_date', None)

            if not name or not seminar_date :
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form3a = Form3A.objects.create(
                user=user,
                name=name,
                seminar_date=seminar_date,
            )

            # # Create Education instances and link them to Form1A
            # for course in courses:
            #     serializer = CourseSerializer(data=course)
            #     if serializer.is_valid():
            #         course_instance = serializer.save()
            #         form3a.course.add(course_instance)
            #     else:
            #         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #         return send_response(result=False, message=serializer.errors)

            form3a.save()

                # Update user's form1a_submitted field
            user.form3a_submitted = timezone.now()
            user.save()
            # return Response(Form1ASerializer(form1a).data, status=status.HTTP_201_CREATED)
            return send_response(result=True, message="Form3A created successfully")
        except Exception as e:
            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
            return send_response(result=False, message=str(e))
        

class form3BView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            name = request.data.get('name', None)
            semester = request.data.get('semester', None)
            session = request.data.get('session', None)
            rollno = request.data.get('rollno', None)
            category = request.data.get('category', None)
            date_of_enrolment = request.data.get('date_of_enrolment', None)
            department = request.data.get('department', None)
            is_registration_completed = request.data.get('is_registration_completed', None)
            permanent_address = request.data.get('permanent_address', None)
            fees_date = request.data.get('fees_date', None)
            area_of_research = request.data.get('area_of_research', None)
            institute_stay_date_from = request.data.get('institute_stay_date_from', None)
            institute_stay_date_to = request.data.get('institute_stay_date_to', None)

            # if not name or not seminar_date :
            #     return send_response(result=False, message="Empty Fields")
            
            if not name or not semester or not session or not rollno or not category or not date_of_enrolment or not department or not permanent_address or not fees_date or not area_of_research or not institute_stay_date_from or not institute_stay_date_to:
                return send_response(result=False, message="Empty Fields")
            
            form3b = Form3B.objects.create(
                user=user,
                name=name,
                semester=semester,
                session=session,
                rollno=rollno,
                category=category,
                date_of_enrolment=date_of_enrolment,
                department=department,
                is_registration_completed=is_registration_completed,
                permanent_address=permanent_address,
                fees_date=fees_date,
                area_of_research=area_of_research,
                institute_stay_date_from=institute_stay_date_from,
                institute_stay_date_to=institute_stay_date_to
            )

            # # Create Education instances and link them to Form1A
            # for course in courses:
            #     serializer = CourseSerializer(data=course)
            #     if serializer.is_valid():
            #         course_instance = serializer.save()
            #         form3b.course.add(course_instance)
            #     else:
            #         # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            #         return send_response(result=False, message=serializer.errors)

            form3b.save()

                # Update user's form1a_submitted field
            user.form3b_submitted = timezone.now()
            user.save()
            # return Response(Form1ASerializer(form1a).data, status=status.HTTP_201_CREATED)
            return send_response(result=True, message="Form3B created successfully")
        except Exception as e:
            # return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)    
            return send_response(result=False, message=str(e))
        

class form3CView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            name = request.data.get('name', None)
            date_of_seminar = request.data.get('date_of_seminar', None)
            branch = request.data.get('branch', None)
            rollno = request.data.get('rollno', None)
            topic_of_talk = request.data.get('topic_of_talk', None)
            progress = request.data.get('progress', None)
            committees = request.data.get('committees', [])

            
            if not name or not date_of_seminar or not branch or not rollno or not topic_of_talk or not committees or not progress:
                return send_response(result=False, message="Empty Fields")
            
            form3c = Form3C.objects.create(
                user=user,
                name=name,
                date_of_seminar=date_of_seminar,
                branch=branch,
                rollno=rollno,
                topic_of_talk=topic_of_talk,
                progress=progress
            )


            # Create Education instances and link them to Form1A
            for committee in committees:
                serializer = CommitteeSerializer(data=committee)
                if serializer.is_valid():
                    committee_instance = serializer.save()
                    form3c.committee.add(committee_instance)
                else:
                    return send_response(result=False, message=serializer.errors)
                
            form3c.save()

            user.form3c_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form3C created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

class form4AView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            name = request.data.get('name', None)
            date_of_seminar = request.data.get('date_of_seminar', None)
            branch = request.data.get('branch', None)
            rollno = request.data.get('rollno', None)
            topic_of_talk = request.data.get('topic_of_talk', None)
            committees = request.data.get('committees', [])

            
            if not name or not date_of_seminar or not branch or not rollno or not topic_of_talk or not committees:
                return send_response(result=False, message="Empty Fields")
            
            form4a = Form4A.objects.create(
                user=user,
                name=name,
                date_of_seminar=date_of_seminar,
                branch=branch,
                rollno=rollno,
                topic_of_talk=topic_of_talk
            )


            # Create Education instances and link them to Form1A
            for committee in committees:
                serializer = CommitteeSerializer(data=committee)
                if serializer.is_valid():
                    committee_instance = serializer.save()
                    form4a.committee.add(committee_instance)
                else:
                    return send_response(result=False, message=serializer.errors)
                
            form4a.save()

            user.form4a_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4A created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

class form4BView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            name = request.data.get('name', None)
            department = request.data.get('department', None)
            thesis_date = request.data.get('thesis_date', None)
            rollno = request.data.get('rollno', None)
            committees = request.data.get('committees', [])

            
            if not name or not department or not thesis_date or not rollno or not committees:
                return send_response(result=False, message="Empty Fields")
            
            form4b = Form4B.objects.create(
                user=user,
                name=name,
                department=department,
                thesis_date=thesis_date,
                rollno=rollno
            )


            # Create Education instances and link them to Form1A
            for committee in committees:
                serializer = CommitteeSerializer(data=committee)
                if serializer.is_valid():
                    committee_instance = serializer.save()
                    form4b.committee.add(committee_instance)
                else:
                    return send_response(result=False, message=serializer.errors)
                
            form4b.save()

            user.form4b_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4B created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

class form4CView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Extract form data from request
            user = request.user
            name = request.data.get('name', None)
            rollno = request.data.get('rollno', None)
            department = request.data.get('department', None)
            date_of_registeration = request.data.get('date_of_registeration', None)
            title_of_thesis = request.data.get('title_of_thesis', None)
            degree = request.data.get('degree', None)
            supervisor = request.data.get('supervisor', None)
            indian_examiner_id = request.data.get('indian_examiner_id', None)
            foreign_examiner_id = request.data.get('foreign_examiner_id', None)
            committees = request.data.get('committees', [])

            if not name or not rollno or not department or not date_of_registeration or not title_of_thesis or not degree or not supervisor or not indian_examiner_id or not foreign_examiner_id or not committees:
                return send_response(result=False, message="Empty Fields")
            
            if not Examiner.objects.filter(pk=indian_examiner_id).exists() or not Examiner.objects.filter(pk=foreign_examiner_id).exists():
                return send_response(result=False, message="Examiner does not exist")
            
            indian_examiner = Examiner.objects.get(pk=indian_examiner_id)
            foreign_examiner = Examiner.objects.get(pk=foreign_examiner_id)
            
            form4c = Form4C.objects.create(
                user=user,
                name=name,
                rollno=rollno,
                department=department,
                date_of_registeration=date_of_registeration,
                title_of_thesis=title_of_thesis,
                degree=degree,
                supervisor=supervisor,
                indian_examiner=indian_examiner,
                foreign_examiner=foreign_examiner
            )


            # Create Education instances and link them to Form1A
            for committee in committees:
                serializer = CommitteeSerializer(data=committee)
                if serializer.is_valid():
                    committee_instance = serializer.save()
                    form4c.committee.add(committee_instance)
                else:
                    return send_response(result=False, message=serializer.errors)
                
            form4c.save()

            user.form4c_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4C created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        


class form4DView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user=request.user
            is_accepted = request.data.get('is_accepted', None)

            if is_accepted is None:
                return send_response(result=False, message="Empty Fields")
            
            form4d = Form4D.objects.create(
                user=user,
                is_accepted=is_accepted
            )
            form4d.save()

            user.form4d_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4D created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

class form4EView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user=request.user
            name_of_author = request.data.get('name_of_author', None)
            title_of_manuscript = request.data.get('title_of_manuscript', None)
            conference_name = request.data.get('conference_name', None)
            year_of_publications = request.data.get('year_of_publications', None)

            if not name_of_author or not title_of_manuscript or not conference_name or not year_of_publications:
                return send_response(result=False, message="Empty Fields")
            
            form4e = Form4E.objects.create(
                user=user,
                name_of_author=name_of_author,
                title_of_manuscript=title_of_manuscript,
                conference_name=conference_name,
                year_of_publications=year_of_publications
            )
            form4e.save()

            user.form4e_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4E created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))


class form5View(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user=request.user
            name = request.data.get('name', None)
            rollno = request.data.get('rollno', None)
            title_of_thesis = request.data.get('title_of_thesis', None)
            is_academic_standard = request.data.get('is_academic_standard', None)
            is_viva = request.data.get('is_viva', None)
            is_modification = request.data.get('is_modification', None)
            is_modification_final = request.data.get('is_modification_final', None)
            is_rejected = request.data.get('is_rejected', None)
            place = request.data.get('place', None)
            name_of_examiner = request.data.get('name_of_examiner', None)
            affliation = request.data.get('affliation', None)
            professor = request.data.get('professor', None)
            
            if not name or not rollno or not title_of_thesis or not is_academic_standard or not is_viva or not is_modification or not is_modification_final or not is_rejected or not place or not name_of_examiner or not affliation or not professor:
                return send_response(result=False, message="Empty Fields")
            
            form5 = Form5.objects.create(
                user=user,
                name=name,
                rollno=rollno,
                title_of_thesis=title_of_thesis,
                is_academic_standard=is_academic_standard,
                is_viva=is_viva,
                is_modification=is_modification,
                is_modification_final=is_modification_final,
                is_rejected=is_rejected,
                place=place,
                name_of_examiner=name_of_examiner,
                affliation=affliation,
                professor=professor
            )
            form5.save()

            user.form5_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form5 created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        


class form6View(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user=request.user
            name = request.data.get('name', None)
            date_of_viva_voce = request.data.get('date_of_viva_voce', None)
            rollno = request.data.get('rollno', None)
            department = request.data.get('department', None)
            title_of_thesis = request.data.get('title_of_thesis', None)
            degree = request.data.get('degree', None)
            indian_examiner = request.data.get('indian_examiner', None)
            foreign_examiner = request.data.get('foreign_examiner', None)
            supervisor = request.data.get('supervisor', None)
            number_of_people = request.data.get('number_of_people', None)
            performance = request.data.get('performance', None)
            comments = request.data.get('comments', [])
            committees = request.data.get('committees', None)
            
            if not name or not date_of_viva_voce or not rollno or not department or not title_of_thesis or not degree or not indian_examiner or not foreign_examiner or not supervisor or not number_of_people or not performance or not comments or not committees:
                return send_response(result=False, message="Empty Fields")
            form6 = Form6.objects.create(
                user=user,
                name=name,
                date_of_viva_voce=date_of_viva_voce,
                rollno=rollno,
                department=department,
                title_of_thesis=title_of_thesis,
                degree=degree,
                indian_examiner=indian_examiner,
                foreign_examiner=foreign_examiner,
                supervisor=supervisor,
                number_of_people=number_of_people,
                performance=performance,
            )

            for committee in committees:
                serializer = CommitteeSerializer(data=committee)
                if serializer.is_valid():
                    committee_instance = serializer.save()
                    form6.committee.add(committee_instance)
                else:
                    return send_response(result=False, message=serializer.errors)
                
            for comment in comments:
                serializer = CommentSerializer(data=comment)
                if serializer.is_valid():
                    comment_instance = serializer.save()
                    form6.comment.add(comment_instance)
                else:
                    return send_response(result=False, message=serializer.errors)
                
            form6.save()

            user.form6_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form6 created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))