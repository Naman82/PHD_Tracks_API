from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


urlpatterns = [
    path('',indexView.as_view(),name="indexView"),
    path('register/user/',userRegistrationView.as_view(),name="userRegistrationView"),
    # path('register/admin/',adminRegisterationView.as_view(),name="adminRegisterationView"),
    path('login/',loginView.as_view(),name="loginView"),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # path('examiner/list/',examinerView.as_view(),name='examinerView'),
    # path('examiner/<int:pk>/update/',examinerView.as_view(),name='examinerView-update'),
    path('user/list/',userListView.as_view(),name='userView-list'),
    path('user/<int:pk>/',userDetailsView.as_view(),name='userView-detail'),
    path('user/<int:pk>/update/',userDetailsView.as_view(),name='userView-update'),

    path('form1A/user/<int:pk>/',form1AView.as_view(),name="Form1AView-Get"),
    # path('form1A/user/',form1AView.as_view(),name="Form1AView"),
    path('form1B/user/<int:pk>/',form1BView.as_view(),name="Form1BView-Get"),
    # path('form1B/user/',form1BView.as_view(),name="Form1BView"),
    path('form2/user/<int:pk>/',form2View.as_view(),name="Form2View-Get"),
    # path('form2/user/',form2View.as_view(),name="Form2View"),
    path('form3A/user/<int:pk>/',form3AView.as_view(),name="Form3AView-Get"),
    # path('form3A/user/',form3AView.as_view(),name="Form3AView"),
    path('form3B/user/<int:pk>/',form3BView.as_view(),name="Form3BView-Get"),
    # path('form3B/user/',form3BView.as_view(),name="Form3BView"),
    path('form3C/user/<int:pk>/',form3CView.as_view(),name="Form3CView-Get"),
    # path('form3C/user/',form3CView.as_view(),name="Form3CView"),
    path('form4A/user/<int:pk>/',form4AView.as_view(),name="Form4AView-Get"),
    # path('form4A/user/',form4AView.as_view(),name="Form4AView"),
    path('form4B/user/<int:pk>/',form4BView.as_view(),name="Form4BView-Get"),
    # path('form4B/user/',form4BView.as_view(),name="Form4BView"),
    path('form4C/user/<int:pk>/',form4CView.as_view(),name="Form4CView-Get"),
    # path('form4C/user/',form4CView.as_view(),name="Form4CView"),
    path('form4D/user/<int:pk>/',form4DView.as_view(),name="Form4DView-Get"),
    # path('form4D/user/',form4DView.as_view(),name="Form4DView"),
    path('form4E/user/<int:pk>/',form4EView.as_view(),name="Form4EView-Get"),
    # path('form4E/user/',form4EView.as_view(),name="Form4EView"),
    path('form5/user/<int:pk>/',form5View.as_view(),name="Form5View-Get"),
    # path('form5/user/',form5View.as_view(),name="Form5View"),
    path('form6/user/<int:pk>/',form6View.as_view(),name="Form6View-Get"),
    # path('form6/user/',form6View.as_view(),name="Form6View"),

    path('user/thesis/list/',ThesisDownloadView.as_view(),name="ThesisDownloadView"),
    path('scholar/list/<int:pk>/',studentsOfProfessor.as_view(),name="studentsOfProfessor"),
    path('professor/list/',professorList.as_view(),name="professorList"),
]