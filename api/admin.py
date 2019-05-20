from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(UserFeedback)
admin.site.register(UserSkill)
admin.site.register(Skill)
admin.site.register(StateReport)
admin.site.register(BackgroundFeedback)
admin.site.register(Company)
admin.site.register(CompanyPolicy)
admin.site.register(Department)
admin.site.register(GeneralManager)
admin.site.register(Manager)
admin.site.register(Profile)
admin.site.register(Staff)

