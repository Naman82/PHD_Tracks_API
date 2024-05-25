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
        
class ThesisDownloadView(APIView):
    def get(self,request):
        try:
            users = User.objects.all()
            data = []
            # print(users)
            for user in users:
                if not user.is_superuser and not user.is_active:
                    if user.supervisor is None:
                        data.append({
                            'id': user.id,
                            'name': user.first_name + ' ' + user.last_name,
                            'roll_no': user.roll_no,
                            'supervisor': 'None',
                            'thesis_url': user.thesis_url,
                            # 'area_of_research':user.area_of_research,
                            'title_of_thesis': user.title_of_thesis
                        })
                    else:
                        data.append({
                            'id': user.id,
                            'name': user.first_name + ' ' + user.last_name,
                            'roll_no': user.roll_no,
                            'supervisor': user.supervisor.first_name + ' ' + user.supervisor.last_name,
                            'thesis_url': user.thesis_url,
                            # 'area_of_research':user.area_of_research,
                            'title_of_thesis': user.title_of_thesis
                        })
            return send_response(result=True, data=data)

        except Exception as e:
            return send_response(result=False, message=str(e))


class userRegistrationView(APIView):
    
    def post(self, request):
        try:
            first_name = request.data.get('first_name', None)
            last_name = request.data.get('last_name', None)
            department = request.data.get('department', None)
            email = request.data.get('email', None)
            user_type = request.data.get('user_type', None)
            password = request.data.get('password', None)
            roll_no = request.data.get('roll_no', None)
            supervisor = request.data.get('supervisor', None)
            if first_name is not None and last_name is not None and email is not None and password is not None and department is not None   and user_type is not None:
                user = User.objects.filter(email=email)
                if not user.exists():
                    if supervisor is not None and  User.objects.filter(pk=supervisor).exists():
                        user = User.objects.get(pk=supervisor)
                        new_user = User.objects.create_user(email=email, first_name=first_name,last_name=last_name, password=password, department=department, roll_no=roll_no, supervisor=user,status='Newbie', user_type=user_type)
                        return send_response(result=True, message="User created successfully")
                    else:
                        new_user = User.objects.create_user(email=email, first_name=first_name,last_name=last_name, password=password, department=department, user_type=user_type)
                        return send_response(result=True, message="User created successfully")
                else:
                    return send_response(result=False, message="User with this email already exists")
            else:
                return send_response(result=False, message="Empty Fields")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

# class adminRegisterationView(APIView):

#     def post(self,request):
#         try:
#             first_name = request.data.get('first_name', None)
#             last_name = request.data.get('last_name', None)
#             email = request.data.get('email', None)
#             password = request.data.get('password', None)
#             if first_name is not None and last_name is not None and email is not None and password is not None:
#                 user = User.objects.filter(email=email)
#                 if not user.exists():
#                     new_user = User.objects.create_superuser(email=email, first_name=first_name,last_name=last_name, password=password)
#                     return send_response(result=True, message="User created successfully")
#                 else:
#                     return send_response(result=False, message="User with this email already exists")
#             else:
#                 return send_response(result=False, message="Empty Fields")
#         except Exception as e:
#             return send_response(result=False,message=str(e))
        


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
        

class userListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            users = User.objects.filter(is_superuser=False)
            return send_response(result=True, data=UserSerializer(users, many=True).data)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
class userDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            user_data = UserSerializer(user).data
            if Form1A.objects.filter(user=user).exists():
                form1a = Form1A.objects.filter(user=user).first()
                form1a_data = Form1ASerializer(form1a).data
                user_data['form1a'] = form1a_data
            if Form1B.objects.filter(user=user).exists():
                form1b = Form1B.objects.filter(user=user).first()
                form1b_data = Form1BSerializer(form1b).data
                user_data['form1b'] = form1b_data
            if Form2.objects.filter(user=user).exists():
                form2 = Form2.objects.filter(user=user).first()
                form2_data = Form2Serializer(form2).data
                user_data['form2'] = form2_data
            if Form3A.objects.filter(user=user).exists():
                form3a = Form3A.objects.filter(user=user).first()
                form3a_data = Form3ASerializer(form3a).data
                user_data['form3a'] = form3a_data
            if Form3B.objects.filter(user=user).exists():
                form3b = Form3B.objects.filter(user=user).first()
                form3b_data = Form3BSerializer(form3b).data
                user_data['form3b'] = form3b_data
            if Form3C.objects.filter(user=user).exists():
                form3c = Form3C.objects.filter(user=user).first()
                form3c_data = Form3CSerializer(form3c).data
                user_data['form3c'] = form3c_data
            if Form4A.objects.filter(user=user).exists():
                form4a = Form4A.objects.filter(user=user).first()
                form4a_data = Form4ASerializer(form4a).data
                user_data['form4a'] = form4a_data
            if Form4B.objects.filter(user=user).exists():
                form4b = Form4B.objects.filter(user=user).first()
                form4b_data = Form4BSerializer(form4b).data
                user_data['form4b'] = form4b_data
            if Form4C.objects.filter(user=user).exists():
                form4c = Form4C.objects.filter(user=user).first()
                form4c_data = Form4CSerializer(form4c).data
                user_data['form4c'] = form4c_data
            if Form4D.objects.filter(user=user).exists():
                form4d = Form4D.objects.filter(user=user).first()
                form4d_data = Form4DSerializer(form4d).data
                user_data['form4d'] = form4d_data
            if Form4E.objects.filter(user=user).exists():
                form4e = Form4E.objects.filter(user=user).first()
                form4e_data = Form4ESerializer(form4e).data
                user_data['form4e'] = form4e_data
            if Form5.objects.filter(user=user).exists():
                form5 = Form5.objects.filter(user=user).first()
                form5_data = Form5Serializer(form5).data
                user_data['form5'] = form5_data
            if Form6.objects.filter(user=user).exists():
                form6 = Form6.objects.filter(user=user).first()
                form6_data = Form6Serializer(form6).data
                user_data['form6'] = form6_data

            return send_response(result=True, data=user_data)

            # return send_response(result=True, data=UserSerializer(user).data)
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
            if 'title_of_thesis' in request.data:
                user.title_of_thesis = request.data.get('title_of_thesis')
            if 'status' in request.data:
                user.status = request.data.get('status')    
            if 'comments_by_indian' in request.data:
                user.comments_by_indian = request.data.get('comments_by_indian')
            if 'comments_by_foreign' in request.data:
                user.comments_by_foreign = request.data.get('comments_by_foreign')
            if 'indian_examiner_id' in request.data:
                indian_examiner=Examiner.objects.get(pk=request.data.get('indian_examiner_id'))
                user.indian_examiner = indian_examiner
            if 'foreign_examiner_id' in request.data:
                foreign_examiner=Examiner.objects.get(pk=request.data.get('foreign_examiner_id'))
                user.foreign_examiner = foreign_examiner
            
            user.save()
            return send_response(result=True, message="User updated successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

class examinerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # examiners = Examiner.objects.filter(is_assigned=False)
            indians = Examiner.objects.filter(is_indian=True)
            foreigners = Examiner.objects.filter(is_indian=False)
            return send_response(result=True, data={'indian': ExaminerSerializer(indians, many=True).data, 'foreign': ExaminerSerializer(foreigners, many=True).data})
            # return send_response(result=True, data=ExaminerSerializer(examiners, many=True).data)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
    # def patch(self,request,pk):
    #     try:
    #         if not Examiner.objects.filter(pk=pk).exists():
    #             return send_response(result=False, message="Examiner does not exist")
    #         examiner = Examiner.objects.get(pk=pk)
    #         if 'is_assigned' in request.data:
    #             examiner.is_assigned = request.data.get('is_assigned')
    #         examiner.save()
    #         return send_response(result=True, message="Examiner updated successfully")
    #     except Exception as e:
    #         return send_response(result=False, message=str(e))
    def post(self,request):
        try:
            serializer = ExaminerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return send_response(result=true, message="Examiner created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
class form1AView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form1A details for the user
            form1a_details = Form1A.objects.filter(user=user).first()
            
            if not form1a_details:
                return send_response(result=False, message="Form1A details not found for this user")
            
            # Serialize the form1a details
            form1a_data = Form1ASerializer(form1a_details).data
            
            return send_response(result=True, data=form1a_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form1a = Form1A.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form1a.save()

             # Update user's form1a_submitted field
            user.form1a_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form1A created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

class form1BView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form1b details for the user
            form1b_details = Form1B.objects.filter(user=user).first()
            
            if not form1b_details:
                return send_response(result=False, message="Form1B details not found for this user")
            
            # Serialize the form1b details
            form1b_data = Form1BSerializer(form1b_details).data
            
            return send_response(result=True, data=form1b_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form1b = Form1B.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form1b.save()

             # Update user's form1a_submitted field
            user.form1b_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form1B created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
class form2View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form2 details for the user
            form2_details = Form2.objects.filter(user=user).first()
            
            if not form2_details:
                return send_response(result=False, message="Form2 details not found for this user")
            
            # Serialize the form2 details
            form2_data = Form2Serializer(form2_details).data
            
            return send_response(result=True, data=form2_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form2 = Form2.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form2.save()

             # Update user's form1a_submitted field
            user.form2_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form2 created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))  
          
class form3AView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form3A details for the user
            form3a_details = Form3A.objects.filter(user=user).first()
            
            if not form3a_details:
                return send_response(result=False, message="Form3A details not found for this user")
            
            # Serialize the form1a details
            form3a_data = Form3ASerializer(form3a_details).data
            
            return send_response(result=True, data=form3a_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form3a = Form3A.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form3a.save()

             # Update user's form1a_submitted field
            user.form3a_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form3A created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        
class form3BView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form3b details for the user
            form3b_details = Form3B.objects.filter(user=user).first()
            
            if not form3b_details:
                return send_response(result=False, message="Form3B details not found for this user")
            
            # Serialize the form1b details
            form3b_data = Form3BSerializer(form3b_details).data
            
            return send_response(result=True, data=form3b_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form3b = Form3B.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form3b.save()

             # Update user's form1a_submitted field
            user.form3b_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form3B created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
class form3CView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form3c details for the user
            form3c_details = Form3C.objects.filter(user=user).first()
            
            if not form3c_details:
                return send_response(result=False, message="Form3C details not found for this user")
            
            # Serialize the form3c details
            form3c_data = Form3CSerializer(form3c_details).data
            
            return send_response(result=True, data=form3c_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form3c = Form3C.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form3c.save()

             # Update user's form1a_submitted field
            user.form3c_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form3C created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
class form4AView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form4a details for the user
            form4a_details = Form4A.objects.filter(user=user).first()
            
            if not form4a_details:
                return send_response(result=False, message="Form4A details not found for this user")
            
            # Serialize the form4a details
            form4a_data = Form4ASerializer(form4a_details).data
            
            return send_response(result=True, data=form4a_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form4a = Form4A.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form4a.save()

             # Update user's form1a_submitted field
            user.form4a_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4A created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
class form4BView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form4b details for the user
            form4b_details = Form4B.objects.filter(user=user).first()
            
            if not form4b_details:
                return send_response(result=False, message="Form4B details not found for this user")
            
            # Serialize the form4b details
            form4b_data = Form4BSerializer(form4b_details).data
            
            return send_response(result=True, data=form4b_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form4b = Form4B.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form4b.save()

             # Update user's form1a_submitted field
            user.form4b_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4B created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
class form4CView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form4c details for the user
            form4c_details = Form4C.objects.filter(user=user).first()
            
            if not form4c_details:
                return send_response(result=False, message="Form4C details not found for this user")
            
            # Serialize the form4c details
            form4c_data = Form4CSerializer(form4c_details).data
            
            return send_response(result=True, data=form4c_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form4c = Form4C.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form4c.save()

             # Update user's form1a_submitted field
            user.form4c_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4C created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

class form4DView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form4d details for the user
            form4d_details = Form4D.objects.filter(user=user).first()
            
            if not form4d_details:
                return send_response(result=False, message="Form4D details not found for this user")
            
            # Serialize the form4d details
            form4d_data = Form4DSerializer(form4d_details).data
            
            return send_response(result=True, data=form4d_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form4d = Form4D.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form4d.save()

             # Update user's form1a_submitted field
            user.form4d_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4D created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
class form4EView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form4e details for the user
            form4e_details = Form4E.objects.filter(user=user).first()
            
            if not form4e_details:
                return send_response(result=False, message="Form4E details not found for this user")
            
            # Serialize the form4e details
            form4e_data = Form4ESerializer(form4e_details).data
            
            return send_response(result=True, data=form4e_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form4e = Form4E.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form4e.save()

             # Update user's form1a_submitted field
            user.form4e_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form4E created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
class form5View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form5 details for the user
            form5_details = Form5.objects.filter(user=user).first()
            
            if not form5_details:
                return send_response(result=False, message="Form5 details not found for this user")
            
            # Serialize the form5 details
            form5_data = Form5Serializer(form5_details).data
            
            return send_response(result=True, data=form5_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form5 = Form5.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form5.save()

             # Update user's form1a_submitted field
            user.form5_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form5 created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))

class form6View(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            # Check if the user exists
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            
            # Fetch Form6 details for the user
            form6_details = Form6.objects.filter(user=user).first()
            
            if not form6_details:
                return send_response(result=False, message="Form6 details not found for this user")
            
            # Serialize the form6 details
            form6_data = Form6Serializer(form6_details).data
            
            return send_response(result=True, data=form6_data)
        except Exception as e:
            return send_response(result=False, message=str(e))
    def post(self, request,pk):
        try:
            # Extract form data from request
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="User does not exist")
            user = User.objects.get(pk=pk)
            softcopy_url = request.data.get('softcopy_url', None)

            if not softcopy_url:
                return send_response(result=False, message="Empty Fields")
            
            # Create Form1A instance
            form6 = Form6.objects.create(
                user=user,
                softcopy_url = softcopy_url
            )
            form6.save()

             # Update user's form1a_submitted field
            user.form6_submitted = timezone.now()
            user.save()
            return send_response(result=True, message="Form6 created successfully")
        except Exception as e:
            return send_response(result=False, message=str(e))
        

class professorList(APIView):
    def get(self,request):
        try:
            professors = User.objects.filter(user_type='professor')
            return send_response(result=True, data=UserSerializer(professors, many=True).data)
        except Exception as e:
            return send_response(result=False, message=str(e))
        
class studentsOfProfessor(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,pk):
        try:
            if not User.objects.filter(pk=pk).exists():
                return send_response(result=False, message="Professor does not exist")
            professor = User.objects.get(pk=pk)
            students = User.objects.filter(supervisor=professor)
            return send_response(result=True, data=UserSerializer(students, many=True).data)
        except Exception as e:
            return send_response(result=False, message=str(e))