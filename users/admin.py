from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register([User, Education, Form1A, Course, Form1B, Form2, Form3A, Form3B, Committee, Form3C, Form4A, Form4B, Examiner, Form4C, Form4D, Form4E, Form5, Form6])