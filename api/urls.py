""""
    docsting for urls
"""
from django.urls import re_path, include
from rest_framework import routers

from api import views as api_views
from api.views import FileUploadView, SocialReport, StaffSkill, StaffFeedback, DepartmentFeedback, CurrentProfile, \
    UserDepartment, DepartmentStaff, UserPageFeedback, UserPageInfo,UserPageSkills, UserPageReports


ROUTER = routers.DefaultRouter()
ROUTER.register(r'users', api_views.UserViewSet)
ROUTER.register(r'profiles', api_views.ProfileViewSet)
ROUTER.register(r'feedbacks', api_views.BackgroundFeedbackViewSet)
ROUTER.register(r'policies', api_views.CompanyPolicyViewSet)
ROUTER.register(r'companies', api_views.CompanyViewSet)
ROUTER.register(r'departments', api_views.DepartmentViewSet)
ROUTER.register(r'generals', api_views.GeneralManagerViewSet)
ROUTER.register(r'managers', api_views.ManagerViewSet)
ROUTER.register(r'staff', api_views.StaffViewSet)
ROUTER.register(r'skills', api_views.SkillViewSet)
ROUTER.register(r'userskills', api_views.UserSkillViewSet)
ROUTER.register(r'reports', api_views.StateReportViewSet)
ROUTER.register(r'userfeedbacks', api_views.UserFeedbackViewSet)


urlpatterns = [
    re_path(r'^', include(ROUTER.urls), name="crud"),
    re_path(r'^upload/(?P<filename>[^/]+)$', FileUploadView.as_view()),
    re_path(r'^report', SocialReport.as_view()),
    re_path(r'^rate_skill', StaffSkill.as_view()),
    re_path(r'^feedback', DepartmentFeedback.as_view()),
    re_path(r'^userfeedback', StaffFeedback.as_view()),
    re_path(r'^current', CurrentProfile.as_view()),
    re_path(r'^department/info/$', UserDepartment.as_view()),
    re_path(r'^department/staff/$', DepartmentStaff.as_view()),
    re_path(r'^user/info/(?P<username>\w{0,50})/$', UserPageInfo.as_view()),
    re_path(r'^user/feedbacks/(?P<username>\w{0,50})/$', UserPageFeedback.as_view()),
re_path(r'^user/reports/(?P<username>\w{0,50})/$', UserPageReports.as_view()),
re_path(r'^user/skills/(?P<username>\w{0,50})/$', UserPageSkills.as_view()),
]
