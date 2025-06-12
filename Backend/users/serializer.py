from rest_framework import serializers
from .models import *

from django.contrib.auth import get_user_model
User=get_user_model()

class LogiSerializer(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()
    def to_representation(self,instance):
        ret=super().to_representation(instance)
        ret.pop('password',None)
        return ret


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data) 
        return user


class GenderdataSerializer(serializers.Serializer):
   

    id = serializers.CharField(source='gender') 
    label = serializers.SerializerMethodField()
    value = serializers.IntegerField()

    def get_label(self, obj):
        gender_map = dict(EmployementDetails.GENDER_CHOICES)  
        return gender_map.get(obj['gender'], obj['gender'])  

class Emp_typedataSerializer(serializers.Serializer):
   

    id = serializers.CharField(source='employement_type') 
    label = serializers.SerializerMethodField()
    value = serializers.IntegerField()

    def get_label(self, obj):
        gender_map = dict(EmployementDetails.employement_type_CHOICES)  
        return gender_map.get(obj['employement_type'], obj['employement_type'])  

class EmployementDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployementDetails
        fields = ['id', 'first_name', 'middle_name', 'last_name', 'email', 'date_of_birth', 'gender',
                  'mobile_number',  'employement_type', 
                   'start_date', 'departements']
   


class Departementserializer(serializers.ModelSerializer):

    class Meta:
        model = Departement
        fields = ['id', 'name_of_departement', 'departement_code', 'description', 'departement_head']

    


class SkillSerializer(serializers.ModelSerializer):
    department = Departementserializer(read_only=True, many=True)  
    department_id = serializers.PrimaryKeyRelatedField(
        queryset=Departement.objects.all(),
        write_only=True,
        many=True,  
        required=False
    )

    class Meta:
        model = Skills
        fields = ['id', 'name_of_skill', 'descriptions', 'location_of_skill_get', 'department', 'department_id']

    def create(self, validated_data):
        department_ids = validated_data.pop('department_id', []) 
        skill = Skills.objects.create(**validated_data)  

        if department_ids:
            skill.department.set(department_ids)  

        return skill

    def update(self, instance, validated_data):
        department_ids = validated_data.pop('department_id', [])  

        for attr, value in validated_data.items():
            setattr(instance, attr, value)  

        if department_ids:
            instance.department.set(department_ids)  

        instance.save()
        return instance

class Empskillserializer(serializers.ModelSerializer):
    employe = EmployementDetailsSerializer(read_only=True)
    skill_optaian = SkillSerializer(read_only=True)

    employe_id = serializers.PrimaryKeyRelatedField(
    queryset=EmployementDetails.objects.all(), write_only=True
)

    skill_optaian_id = serializers.PrimaryKeyRelatedField(
        queryset=Skills.objects.all(), write_only=True,
    )

    class Meta:
        model = EmployeSkill
        fields = ['id', 'skill_optaian', 'skill_optaian_id', 'proficions', 'employe', 'employe_id']

    def create(self, validated_data):
        employe_id = validated_data.pop('employe_id', None)
        skill_optaian_id = validated_data.pop('skill_optaian_id', None)
        empskill = EmployeSkill.objects.create(**validated_data)

        if employe_id:
            empskill.employe = employe_id
        if skill_optaian_id:
            empskill.skill_optaian = skill_optaian_id

        empskill.save()
        return empskill

    def update(self, instance, validated_data):
        employe_id = validated_data.pop('employe_id', None)
        skill_optaian_id = validated_data.pop('skill_optaian_id', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if employe_id:
            instance.employe = employe_id
        if skill_optaian_id:
            instance.skill_optaian = skill_optaian_id

        instance.save()
        return instance
