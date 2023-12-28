# blog/urls.py
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views,lmtUtils

urlpatterns = [
    # re_path(r'^articles/$', views.article_list),
    # re_path(r'^articles/(?P<pk>[0-9]+)$', views.article_detail),
    re_path(r'^lmt/$', views.lmtApiview.as_view()),
    re_path(r'^lmt/(?P<pk>[0-9]+)$', views.StudentDerailApiview.as_view()),
    re_path('test/', views.process_value),

]

urlpatterns = format_suffix_patterns(urlpatterns)
