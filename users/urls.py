from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *


urlpatterns = [
    path('',indexView.as_view(),name="indexView"),
    path('register/user/',userRegistrationView.as_view(),name="userRegistrationView"),
    path('register/admin/',adminRegisterationView.as_view(),name="adminRegisterationView"),
    path('login/',loginView.as_view(),name="loginView"),
    path('token-refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('examiner/list/',examinerView.as_view(),name='examinerView'),
    path('examiner/<int:pk>/update/',examinerView.as_view(),name='examinerView-update'),
    path('user/list/',userView.as_view(),name='userView-list'),
    path('user/<int:pk>/',userView.as_view(),name='userView-detail'),
    path('user/<int:pk>/update/',userView.as_view(),name='userView-update'),

    path('form1A/user/<int:pk>/',form1AView.as_view(),name="Form1AView-Get"),
    path('form1A/user/',form1AView.as_view(),name="Form1AView"),
    path('form1B/user/',form1BView.as_view(),name="Form1BView"),
    path('form2/user/',form2View.as_view(),name="Form2View"),
    path('form3A/user/',form3AView.as_view(),name="Form3AView"),
    path('form3B/user/',form3BView.as_view(),name="Form3BView"),
    path('form3C/user/',form3CView.as_view(),name="Form3CView"),
    path('form4A/user/',form4AView.as_view(),name="Form4AView"),
    path('form4B/user/',form4BView.as_view(),name="Form4BView"),
    path('form4C/user/',form4CView.as_view(),name="Form4CView"),
    path('form4D/user/',form4DView.as_view(),name="Form4DView"),
    path('form4E/user/',form4EView.as_view(),name="Form4EView"),
    path('form5/user/',form5View.as_view(),name="Form5View"),
    path('form6/user/',form6View.as_view(),name="Form6View"),
]