from django.urls import path,re_path
from . import LogsViews,SSHViews
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    re_path(r'^logs/$', LogsViews.lmtApiview.as_view()),
    re_path(r'^logs/(?P<pk>[0-9]+)$', LogsViews.StudentDerailApiview.as_view()),
    re_path(r'view_dir/$', LogsViews.view_dir),
    re_path(r'view_log/$', LogsViews.view_log),

]
urlpatterns = format_suffix_patterns(urlpatterns)