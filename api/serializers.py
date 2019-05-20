from rest_framework import serializers
from .models import *


class ProfileSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    class Meta:
        model = Profile
        fields = ('gender', 'birthday', 'social_link')


class UserFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFeedback
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    responsibilities = CustomMultipleChoiceField(choices=ResponsibilityTypes.choices())
    class Meta:
        model = Skill
        fields = '__all__'


class UserSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)

    class Meta:
        model = UserSkill
        fields = '__all__'


class StateReportSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type_display')
    class Meta:
        model = StateReport
        fields = '__all__'


class BackgroundFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = BackgroundFeedback
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class CompanyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPolicy
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    company = CompanySerializer(read_only=True)

    class Meta:
        model = Department
        fields = '__all__'


class GeneralManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralManager
        fields = '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """
    Serializer for User model
    """
    profile = ProfileSerializer(required=True)

    class Meta:
        """
        Settings for serializer
        """
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'is_manager', 'is_director', 'is_staff',
                  'profile')

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        other = validated_data.pop('other')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        Profile.objects.create(user=user, **profile_data)
        department = Department.objects.get(id=other['department_id'])
        if (user.is_manager):
            Manager.objects.create(department=department, user=user, occupation=other['occupation'],
                                   responsibility=other['responsibility'])
        else:
            Staff.objects.create(department=department, user=user, occupation=other['occupation'],
                                 responsibility=other['responsibility'])

        return user

    def validate(self, data):
        if 'profile' in data:
            data['profile'] = ProfileSerializer().validate(data['profile'])

        return {key: value for key, value in data.items() if key in self.fields or key == 'other'}


class ManagerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    responsibility = serializers.CharField(source='get_responsibility_display')

    class Meta:
        model = Manager
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    responsibility = serializers.CharField(source='get_responsibility_display')
    class Meta:
        model = Staff
        fields = '__all__'


