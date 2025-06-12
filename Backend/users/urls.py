
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path,include


router=DefaultRouter()
router.register('register',RegisterViewsets,basename='Register')
router.register('login',LoginViewset,basename='login')
router.register('user',UserViewsets,basename='User')
router.register('skill',SkillsViewSet,basename='skill')
router.register('empdetails',Empviewsets,basename='empdetails')
router.register('departement',Depviewsets,basename='departement')
router.register('empskill',empskillviewsets,basename='empskill')
router.register('genderdata',Genderviewsets,basename='genderdata')
router.register('emp_type',EmployementTypeviewsets,basename='emp_type')


urlpatterns = [ 
    path('', include(router.urls)), 
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('', include(router.urls)), 
    path('', include(router.urls)),
    path('', include(router.urls)),
    path('', include(router.urls)), 
    path('', include(router.urls)), 




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

