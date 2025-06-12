from django.contrib import admin
from .models import *
# Register your models here.
class employe_detials_admin(admin.ModelAdmin):
    list_display=('first_name','middle_name','gender')
class employe_depat_admin(admin.ModelAdmin):
    list_display=('name_of_departement','departement_code','departement_head')
    list_display_links=('departement_code',)
class skill_admin (admin.ModelAdmin):
    list_display=('name_of_skill','location_of_skill_get')  
class emp_skill(admin.ModelAdmin):
    list_display=('employe','proficions') 

admin.site.register(CustomUser)
admin.site.register(EmployementDetails,employe_detials_admin)
admin.site.register(Departement,employe_depat_admin)
admin.site.register(Skills,skill_admin)
admin.site.register(EmployeSkill,emp_skill)