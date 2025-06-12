from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Permission,Group

from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinLengthValidator
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.utils.html import strip_tags



class customUserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError('Email is requird field')
        email=self.normalize_email(email)
        users=self.model(email=email,**extra_fields)
        users.set_password(password)
        users.save(using=self._db)
        return users
    def create_superuser(self,email,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        return self.create_user(email,password,**extra_fields)
class CustomUser(AbstractUser):
    email = models.EmailField(max_length=200, unique=True)
    profile = models.ImageField(upload_to='Admin_images/', blank=True, null=True)
    username = models.CharField(max_length=200, blank=True, null=True)
    
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions', 
        blank=True,
        help_text='Specific permissions for this user.'
    )
    groups = models.ManyToManyField(
          Group,
        related_name='custom_users',
        blank=True,
       help_text='The groups this user belongs to.'
    )
    
    objects = customUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []



import random
import string
from django.db import models

def unique_id():
    """ Generates a unique employee ID """
    prefix = 'I4U'
    middle = '/'
    suffix = ''.join(random.choices(string.digits, k=10))
    return f'{prefix}{middle}{suffix}'


class EmployementDetails(models.Model):
    
    GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('others','Others')
     ]
  


    employement_type_CHOICES = [
    ('full_time', 'Full-Time'),
    ('par_time', 'Part-Time'),
    ('contract','contract'),
    ('filexble','Filexble')
]
    first_name=models.CharField(max_length=70)
    middle_name=models.CharField(max_length=70)
    last_name=models.CharField(max_length=70)
    email=models.EmailField(unique=True)
    date_of_birth=models.DateField()
    gender=models.CharField(max_length=10,choices=GENDER_CHOICES)
    mobile_number=models.CharField(max_length=30)
    employement_type=models.CharField(max_length=23,choices=employement_type_CHOICES)
    start_date=models.DateTimeField()
    departements = models.ForeignKey('Departement', on_delete=models.CASCADE, blank=True, null=True)  
    Isdelete=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    class meta:
        verbose_name='Employement Detial'
        verbose_name_pulural='Employement Detials'

  

    def __str__(self):
        return f'{self.first_name}' 
 


       

class Departement(models.Model):
    name_of_departement=models.CharField(max_length=120,unique=True)
    departement_code=models.CharField(max_length=30,unique=True)
    departement_head=models.OneToOneField('EmployementDetails',null=True,blank=True,on_delete=models.SET_NULL, related_name='head_of_departement')
    description=models.TextField()
    Isdelete=models.BooleanField(default=False)

    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name_of_departement
    
class Skills(models.Model):
    skill_get=[
        ('remote','Remote'),
        ('onsite','Onsite'),
        ( 'hybrid','Hybrid')
    ]

    name_of_skill=models.CharField(max_length=36)
    descriptions=models.TextField()
    department=models.ManyToManyField('Departement',max_length=30)
    location_of_skill_get=models.CharField(max_length=45,choices=skill_get)
    def __str__(self):
        return self.name_of_skill
class EmployeSkill(models.Model):
    knowladge_level=[

        ('Advanced','advanced'),
        ('middle_level','middle_level'),
        ('Beginer','Beginer')
    ]
    employe = models.ForeignKey(
    EmployementDetails, on_delete=models.CASCADE, null=True, blank=True
)

    skill_optaian=models.ForeignKey(Skills,on_delete=models.CASCADE,null=True, blank=True)
    proficions=models.CharField(max_length=200,choices=knowladge_level)
    def __str__(self):
        return f'{self.employe}{self.skill_optaian}'
    



@receiver(reset_password_token_created)
def password_reset_token_created( reset_password_token,*args, **kwargs):
    sitelink="http://localhost:5173/"
    token="{}".format(reset_password_token.key)
    full_link=str(sitelink)+str('password-reset/')+str(token)

    print(token)
    print(full_link)
    context={

        'full_link':full_link,
        'email_address':reset_password_token.user.email

    }
    html_message=render_to_string('backend/email.html',context=context)
    plain_message=strip_tags(html_message)
    msg=EmailMultiAlternatives(
        subject=" You Are Requesting for reset password or Creating Password for {title}".format(title=reset_password_token.user.email),
        body=plain_message,
        from_email='getahuntamirat08@gmail.com',
        to=[reset_password_token.user.email]
    )
    msg.attach_alternative(html_message,"text/html")
    msg.send()
    

   