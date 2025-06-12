from django.shortcuts import render
from rest_framework import viewsets,permissions
from .serializer import*
from .models import *

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.hashers import check_password
#from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework.response import Response
from django.contrib.auth import logout
from django.db.models import Count
from rest_framework.response import Response
from django.contrib.auth import get_user_model,authenticate
from knox.models import AuthToken
from django.core.mail import send_mail

User=get_user_model()




class LoginViewset(viewsets.ViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class=LogiSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            user = authenticate(request, email=email, password=password)
            if user:

                _, token = AuthToken.objects.create(user)
                return Response({
                    "user": self.serializer_class(user).data,
                    "token": token
                })
            else:
                return Response({"error": "Invalid credentials"}, status=401)

        return Response(serializer.errors, status=400)

  

class RegisterViewsets(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)

            return Response({
                "user": self.serializer_class(user).data,
                "token": token  
            })
        return Response(serializer.errors, status=400)



    
       
        
class UserViewsets(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset=User.objects.all()
    serializer_class=RegisterSerializer 
    def list(self, request):
        display =User.objects.all()
        serializer = self.serializer_class(display, many=True)
        return Response(serializer.data)    
    def retrieve(self, request, pk=None):
        try:
            i4u = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "Employe not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(i4u)
        return Response(serializer.data)
class Genderviewsets(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    queryset=EmployementDetails.objects.all()
    serializer_class=GenderdataSerializer

    def list(self, request):
        queryset = EmployementDetails.objects.filter(Isdelete=False).values('gender').annotate(value=Count('gender'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
       
class EmployementTypeviewsets(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    queryset=EmployementDetails.objects.all()
    serializer_class=Emp_typedataSerializer

    def list(self, request):
        queryset = EmployementDetails.objects.filter(Isdelete=False).values('employement_type').annotate(value=Count('employement_type'))
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
    
       

class Empviewsets(viewsets.ViewSet):
    #permission_classes = [IsAuthenticated]
    queryset=EmployementDetails.objects.all()
    serializer_class=EmployementDetailsSerializer

    def list(self, request):
        queryset = self.queryset.filter(Isdelete=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            i4u = self.queryset.get(pk=pk)
        except EmployementDetails.DoesNotExist:
            return Response({"error": "Employe not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(i4u)
        return Response(serializer.data)


    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        try:
            i4u = self.queryset.get(pk=pk)
        except EmployementDetails.DoesNotExist:
            return Response({"error": "Employe not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(i4u, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:

            I4u = self.queryset.get(pk=pk)
            I4u.Isdelete=True
            I4u.save()
            return Response(status=204)
        except EmployementDetails.DoesNotExist:

            return Response({"error": "Not found"}, status=404)
              

class Depviewsets(viewsets.ViewSet):
    queryset = Departement.objects.all()
    serializer_class = Departementserializer

    def list(self, request):
        queryset = self.queryset.filter(Isdelete=False)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            i4u = self.queryset.get(pk=pk)
        except Departement.DoesNotExist:
            return Response({"error": "Departement not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(i4u)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            i4u = self.queryset.get(pk=pk)
        except Departement.DoesNotExist:
            return Response({"error": "Departement not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(i4u, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:

            I4u = self.queryset.get(pk=pk)
            I4u.Isdelete=True
            I4u.save()
            return Response(status=204)
        except EmployementDetails.DoesNotExist:

            return Response({"error": "Not found"}, status=404)

class SkillsViewSet(viewsets.ViewSet):
   # permission_classes = [IsAuthenticated]
    queryset = Skills.objects.all()
    serializer_class = SkillSerializer

    def list(self, request):
        display = self.queryset
        serializer = self.serializer_class(display, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  
        
        I4u = self.queryset.get(pk=pk)
        
        serializer = self.serializer_class(I4u)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        
        I4u = self.queryset.get(pk=pk)
        

        serializer = self.serializer_class(I4u, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        
        I4u = self.queryset.get(pk=pk)
        I4u.delete()
        return Response(status=204)
     
class empskillviewsets(viewsets.ViewSet):
   # permission_classes = [IsAuthenticated]  
    queryset=EmployeSkill.objects.all()
    serializer_class=Empskillserializer
    def list(self, request):
        display = self.queryset
        serializer = self.serializer_class(display, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):  
        
        I4u = self.queryset.get(pk=pk)
        
        serializer = self.serializer_class(I4u)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        
        I4u = self.queryset.get(pk=pk)
        

        serializer = self.serializer_class(I4u, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk=None):
        
        I4u = self.queryset.get(pk=pk)
        I4u.delete()
        return Response(status=204)

def send_email():
    subject = 'Hello from Django'
    message = 'This is a test email sent from Django.'
    sender = 'i4 u emgs'
    recipient = ['getaguntamirat08@gmail.com']  

    send_mail(subject, message, sender, recipient)

    print("Email sent successfully!")
