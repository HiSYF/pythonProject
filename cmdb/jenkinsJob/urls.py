# blog/urls.py
from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # re_path(r'^articles/$', views.article_list),
    # re_path(r'^articles/(?P<pk>[0-9]+)$', views.article_detail),
    re_path(r'^JkBase/$', views.JenkinsApiview.as_view()),
    re_path(r'^jenkinsJob/$', views.JkjobApiview.as_view()),

    re_path(r'^jenkinsJob/(?P<pk>[0-9]+)$', views.JenkinsDerailApiview.as_view()),
    re_path(r'initJob/$', views.initJob),

    # re_path('test/', views.process_value),

]

urlpatterns = format_suffix_patterns(urlpatterns)
