from io import TextIOWrapper

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from api.utils.parser import CSVParser
from api.utils.user_manager import UserManager
from .serializers import *
from .utils.nltk_tools import *
from .utils.social_analyzer import SocialAnalizer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for USERS
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for PROFILES
    """
    queryset = Profile.objects.all().order_by('-date_joined')
    serializer_class = ProfileSerializer


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = Company.objects.all().order_by('-date_joined')
    serializer_class = CompanySerializer


class UserFeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for UserFeedbacks
    """
    queryset = UserFeedback.objects.all().order_by('-date_joined')
    serializer_class = UserFeedbackSerializer


class UserSkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = UserSkill.objects.all().order_by('-date_joined')
    serializer_class = UserSkillSerializer


class SkillViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = Skill.objects.all().order_by('-date_joined')
    serializer_class = SkillSerializer


class StateReportViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = StateReport.objects.all().order_by('-date_joined')
    serializer_class = StateReportSerializer


class BackgroundFeedbackViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = BackgroundFeedback.objects.all().order_by('-date_joined')
    serializer_class = BackgroundFeedbackSerializer


class CompanyPolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = CompanyPolicy.objects.all().order_by('-date_joined')
    serializer_class = CompanyPolicySerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = Department.objects.all().order_by('-date_joined')
    serializer_class = DepartmentSerializer


class GeneralManagerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = GeneralManager.objects.all().order_by('-date_joined')
    serializer_class = GeneralManagerSerializer


class ManagerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = Manager.objects.all().order_by('-date_joined')
    serializer_class = ManagerSerializer


class StaffViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Companies
    """
    queryset = Staff.objects.all().order_by('-date_joined')
    serializer_class = StaffSerializer


class FileUploadView(APIView):
    """
    API endpoint for CSV File upload
    """

    def post(self, request, filename, format=None):

        file = TextIOWrapper(request.FILES[filename].file, encoding=request.encoding)

        user_data = CSVParser.read_from_memory(file)

        user_serializer = UserSerializer()

        response = []

        for user in user_data:

            current_user = UserManager.to_user_data(user)
            verified_data = user_serializer.validate(current_user)
            responce_data = verified_data.copy()
            print(verified_data['username'])
            try:
                existing_user = User.objects.get(username=verified_data['username'])
            except User.DoesNotExist:
                user_serializer.create(verified_data)
            else:
                responce_data['error'] = str(existing_user.username) + ' already exists'
            response.append(responce_data)

        return JsonResponse(response, safe=False)


class DepartmentStaff(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        occupation = None
        if user.is_manager:
            occupation = Manager.objects.get(user=user)
        else:
            occupation = Staff.objects.get(user=user)

        staff = Staff.objects.filter(department=occupation.department)
        managers = Manager.objects.filter(department=occupation.department)
        response = {'staff': StaffSerializer(staff, many=True).data,
                    'managers': ManagerSerializer(managers, many=True).data}

        return JsonResponse(response, safe=False)

    def post(self, request, format=None):
        """
            Add new staff in department
        """

        user_serializer = UserSerializer()

        current_user = UserManager.to_user_data(request.data)
        verified_data = user_serializer.validate(current_user)
        response_data = verified_data.copy()

        try:
            existing_user = User.objects.get(username=verified_data['username'])
        except User.DoesNotExist:
            user_serializer.create(verified_data)
        else:
            response_data['error'] = str(existing_user.username) + ' already exists'

        return JsonResponse(response_data)


class StaffSkill(APIView):

    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """

        """

        user = User.objects.get(id=request.data['user_id'])

        try:
            skill = Skill.objects.get(title=request.data['skill_title'])
        except Skill.DoesNotExist:
            skill = Skill.objects.create(title=request.data['skill_title'], type=0, responsibilities=['OT'])
            user_skill = UserSkill.objects.create(user=user, skill=skill, rating=request.data['rating'], grade_count=1)
        else:
            try:
                user_skill = UserSkill.objects.get(skill=skill)
            except UserSkill.DoesNotExist:
                user_skill = UserSkill.objects.create(user=user, skill=skill, rating=request.data['rating'],
                                                      grade_count=1)
            else:
                user_skill.rating = (user_skill.rating * user_skill.grade_count + request.data['rating']) / (
                        user_skill.grade_count + 1)
                user_skill.grade_count += 1
                user_skill.save()
        serializer = UserSkillSerializer(user_skill)
        return JsonResponse(serializer.data)


class SocialReport(APIView):

    # permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        user_profile = Profile.objects.get(user_id=request.data['id'])
        analizer = SocialAnalizer()
        tweets_reports = analizer.analyze_users_twitter(user_profile.social_link)
        report = dict()
        polarity, subjectivity = 0, 0
        for tweet in tweets_reports:
            polarity += tweet['polarity']
            subjectivity += tweet['subjectivity']
        report['tweets_reports'] = tweets_reports
        report['polarity'] = polarity / len(tweets_reports)
        report['subjectivity'] = subjectivity / len(tweets_reports)

        StateReport.objects.create(user_id=request.data['id'], research=report,
                                   type=0)  # TODO: types from enams not define
        return JsonResponse(report)


class HealthReport(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        pass


class CurrentProfile(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        profile = Profile.objects.get(user=user)
        response = UserSerializer(user).data
        response['profile'] = ProfileSerializer(profile).data
        return JsonResponse(response)


class StaffFeedback(APIView):
    #permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        """

        """

        feedback = request.data['feedback']
        user = User.objects.get(id=request.data['user_id'])
        keywords = get_keywords(feedback)
        analysis = analyze_sentiment(feedback)
        sentiment, polarity, subjectivity = analysis['sentiment'], analysis['polarity'], analysis['subjectivity']
        user_feedback = UserFeedback.objects.create(user=user, feedback=feedback, keywords=keywords,
                                                    sentiment=sentiment, polarity=polarity, subjectivity=subjectivity)
        serializer = UserFeedbackSerializer(user_feedback)

        return JsonResponse(serializer.data)


class UserDepartment(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(id=request.user.id)
        occupation = None
        if user.is_manager:
            occupation = Manager.objects.get(user=user)
        else:
            occupation = Staff.objects.get(user=user)

        department = Department.objects.get(id=occupation.department_id)

        return JsonResponse(DepartmentSerializer(department).data, safe=False)


class DepartmentFeedback(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        user = User.objects.get(id=request.user.id)
        occupation = None
        if user.is_manager:
            occupation = Manager.objects.get(user=user)
        else:
            occupation = Staff.objects.get(user=user)

        feedbacks = BackgroundFeedback.objects.filter(department=occupation.department)
        return JsonResponse(BackgroundFeedbackSerializer(feedbacks, many=True).data, safe=False)

    def post(self, request, format=None):
        """

        """

        feedback = request.data['feedback']
        satisfaction = request.data['satisfaction']
        department = Department.objects.get(id=request.data['department_id'])
        keywords = get_keywords(feedback)
        analysis = analyze_sentiment(feedback)
        sentiment, polarity, subjectivity = analysis['sentiment'], analysis['polarity'], analysis['subjectivity']
        bk_feedback = BackgroundFeedback.objects.create(department=department, feedback=feedback, keywords=keywords,
                                                        sentiment=sentiment, polarity=polarity,
                                                        subjectivity=subjectivity,
                                                        satisfaction=satisfaction)
        serializer = BackgroundFeedbackSerializer(bk_feedback)

        return JsonResponse(serializer.data)


class UserPageSkills(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, username):

        user = User.objects.get(username=username)
        skills = UserSkill.objects.filter(user=user)
        return JsonResponse(UserSkillSerializer(skills, many=True).data, safe=False)


class UserPageInfo(APIView):
    #permission_classes = (IsAuthenticated,)

    def get(self, request, username):

        user = User.objects.get(username=username)
        response = None
        if user.is_manager:
            response = ManagerSerializer(Manager.objects.get(user=user)).data
        else:
            response = StaffSerializer(Staff.objects.get(user=user)).data


        return JsonResponse(response, safe=False)


class UserPageFeedback(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):

        user = User.objects.get(username=username)

        feedbacks = UserFeedback.objects.filter(user=user)
        return JsonResponse(UserFeedbackSerializer(feedbacks, many=True).data, safe=False)


class UserPageReports(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):

        user = User.objects.get(username=username)

        reports = StateReport.objects.filter(user=user)
        return JsonResponse(StateReportSerializer(reports, many=True).data, safe=False)



