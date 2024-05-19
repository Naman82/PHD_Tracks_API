from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MaxValueValidator
import os, uuid

from .managers import UserManager
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):

    def get_update_filename(self, filename):
        ext = filename.split('.')[-1]
        filename = "%s.%s" % (uuid.uuid4(), ext)
        return os.path.join('uploads/user/profile', filename)
    
    username = None
    email = models.EmailField(_('email address'), unique=True)
    profile_pic = models.ImageField(upload_to=get_update_filename, default='uploads/user/profile/default_profile.jpg')
    area_of_research = models.TextField(null=True,blank=True)
    department = models.CharField(max_length=255,null=True,blank=True)
    designation = models.CharField(max_length=255,null=True,blank=True)
    supervisor = models.CharField(max_length=255,null=True,blank=True)
    status = models.CharField(max_length=255,null=True,blank=True)
    thesis_url = models.URLField(null=True,blank=True)
    form1a_submitted = models.DateTimeField(null=True,blank=True)
    form1b_submitted = models.DateTimeField(null=True,blank=True)
    form2_submitted = models.DateTimeField(null=True,blank=True)
    form3a_submitted = models.DateTimeField(null=True,blank=True)
    form3b_submitted = models.DateTimeField(null=True,blank=True)
    form3c_submitted = models.DateTimeField(null=True,blank=True)
    form4a_submitted = models.DateTimeField(null=True,blank=True)
    form4b_submitted = models.DateTimeField(null=True,blank=True)
    form4c_submitted = models.DateTimeField(null=True,blank=True)
    form4d_submitted = models.DateTimeField(null=True,blank=True)
    form4e_submitted = models.DateTimeField(null=True,blank=True)
    form5_submitted = models.DateTimeField(null=True,blank=True)
    form6_submitted = models.DateTimeField(null=True,blank=True)

    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return "{},{},{}".format(self.email, self.first_name, self.last_name)

class Education(models.Model):
    standard = models.CharField(max_length=255)
    university = models.TextField()
    degree = models.TextField()
    year_of_passing = models.TextField()
    cgpa = models.TextField()
    subjects = models.TextField()

    def __str__(self):
        return f"{self.standard} - {self.university} - {self.degree}"


class Form1A(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    education = models.ManyToManyField(Education)
    area_of_research = models.TextField()
    category_of_studentship = models.CharField(max_length=255)
    recommender_1 = models.CharField(max_length=255)
    recommender_2 = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.department} - {self.rollno}"

class Course(models.Model):
    subject_id = models.CharField(max_length=255)
    course_title = models.CharField(max_length=255)
    credits = models.TextField()
    remarks = models.TextField()

class Form1B(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    date_of_enrolment = models.DateField()
    area_of_research = models.TextField()
    category_of_studentship = models.CharField(max_length=255)
    course = models.ManyToManyField(Course)

    def __str__(self):
        return f"{self.name} - {self.department} - {self.rollno}"

class Form2(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    month_year = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    date_of_joining = models.DateTimeField(default=timezone.now)
    work_done = models.IntegerField()
    nature_of_work = models.TextField()
    remarks_by_supervisor = models.TextField()

    def __str__(self):
        return f"{self.name} - {self.department} - {self.rollno}"
    

class Form3A(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    seminar_date = models.DateField()

    def __str__(self):
        return self.name
    
class Form3B(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    semester = models.CharField(max_length=255)
    session = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    date_of_enrolment = models.DateField()
    department = models.CharField(max_length=255)
    is_registration_completed = models.BooleanField(default=False)
    permanent_address = models.TextField()
    fees_date = models.DateField()
    area_of_research = models.TextField()
    institute_stay_date_from = models.DateField()
    institute_stay_date_to = models.DateField()


class Committee(models.Model):
    name = models.CharField(max_length=255)
    remarks = models.TextField(null=True,blank=True)


class Form3C(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    date_of_seminar = models.DateField()
    branch = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    topic_of_talk = models.TextField()
    committee = models.ManyToManyField(Committee)


class Form4A(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    committee = models.ManyToManyField(Committee)


class Form4B(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    thesis_date = models.DateField()
    committee = models.ManyToManyField(Committee)

class Examiner(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    institute = models.TextField()
    areas_of_interest = models.TextField()
    address = models.TextField()
    phone = models.CharField(max_length=13)
    email = models.EmailField()

class Form4C(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    date_of_registeration = models.DateField()
    title_of_thesis = models.CharField(max_length=255)
    degree = models.TextField()
    supervisor = models.CharField(max_length=255)
    indian_examiner = models.ForeignKey(Examiner,on_delete=models.CASCADE, related_name="indianExaminer")
    foreign_examiner = models.ForeignKey(Examiner,on_delete=models.CASCADE, related_name="foreignExaminer")
    committee = models.ManyToManyField(Committee)

class Form4D(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)


class Form4E(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    name_of_author = models.TextField()
    title_of_manuscript = models.TextField()
    conference_name = models.TextField()
    year_of_publications = models.TextField()


class Form5(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    title_of_thesis = models.CharField(max_length=255)
    is_academic_standard = models.BooleanField(default=False)
    is_viva = models.BooleanField(default=False)
    is_modification = models.BooleanField(default=False)
    is_modification_final = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    place = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True)
    name_of_examiner = models.CharField(max_length=255)
    affliation = models.TextField()
    professor = models.CharField(max_length=255)


class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Form6(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    date_of_viva_voce = models.DateField()
    name = models.CharField(max_length=255)
    rollno = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    title_of_thesis = models.CharField(max_length=255)
    degree = models.TextField()
    indian_examiner = models.TextField()
    foreign_examiner = models.TextField()
    supervisor = models.TextField()
    number_of_people = models.IntegerField()
    performance = models.TextField()
    comment = models.ManyToManyField(Comment)
    committee = committee = models.ManyToManyField(Committee)

