from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer
from rest_framework_jwt.views import verify_jwt_token


SCHEMA_VIEW = get_schema_view(title='RATESKILL API',
                              renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^auth/', include('rest_auth.urls')),
    re_path(r'^auth/registration/', include('rest_auth.registration.urls')),
    re_path(r'^schema/', SCHEMA_VIEW, name="docs"),
    re_path(r'^api/', include('api.urls')),
    re_path(r'^api-token-verify/', verify_jwt_token),
]
