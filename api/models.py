from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.fields import JSONField
from django.db import models

from utils.model_fields import ChoiceArrayField, CustomMultipleChoiceField
from .enums import *


class Skill(models.Model):
    title = models.CharField(max_length=100)
    type = models.PositiveSmallIntegerField(choices=SkillTypes.choices(), default=SkillTypes.other)
    responsibilities = ChoiceArrayField(
        models.CharField(choices=ResponsibilityTypes.choices(), max_length=2, blank=True,
                         default=ResponsibilityTypes.other),
    )


class User(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_director = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=True)
    skills = models.ManyToManyField(Skill, through='UserSkill')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.PositiveSmallIntegerField(choices=GenderTypes.choices(), default=GenderTypes.other)
    social_link = models.CharField(max_length=180, default='', blank=True)


class StateReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.PositiveSmallIntegerField(choices=StateReportTypes.choices(), default=StateReportTypes.health)
    research = JSONField()


class UserFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    feedback = models.TextField()
    keywords = ArrayField(models.CharField(max_length=100, blank=True))
    sentiment = models.CharField(max_length=50)
    polarity = models.FloatField()
    subjectivity = models.FloatField()


class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    grade_count = models.PositiveIntegerField()
    rating = models.FloatField()


class Company(models.Model):
    name = models.CharField(max_length=140)
    type = models.CharField(max_length=200)
    country = models.CharField(max_length=2, choices=COUNTRIES, default='UA')


class CompanyPolicy(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, primary_key=True)
    banned_tags = ArrayField(models.CharField(max_length=100, blank=True))


class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=140)
    type = models.CharField(max_length=2, choices=DepartmentTypes.choices(), default=DepartmentTypes.other)


class BackgroundFeedback(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now=True)
    feedback = models.TextField()
    keywords = ArrayField(models.CharField(max_length=100, blank=True))
    sentiment = models.CharField(max_length=50)
    polarity = models.FloatField()
    subjectivity = models.FloatField()
    satisfaction = models.PositiveSmallIntegerField()


class Manager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=120)
    responsibility = models.CharField(choices=ResponsibilityTypes.choices(),
                                      default=ResponsibilityTypes.other, max_length=2)


class GeneralManager(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=120)
    responsibility = models.CharField(choices=ResponsibilityTypes.choices(),
                                      default=ResponsibilityTypes.other, max_length=2)


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=120)
    responsibility = models.CharField(choices=ResponsibilityTypes.choices(),
                                      default=ResponsibilityTypes.other, max_length=2)
