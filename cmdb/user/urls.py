from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views,MyObtainTokenPairView

urlpatterns = [
    re_path(r'^token/$', MyObtainTokenPairView.MyObtainTokenPairView.as_view()),
    re_path(r'^user/info/$', views.ArticleUserInfo.as_view()),
    re_path('getPubKey/', views.getPubKey),


    # re_path(r'^articles/$', views.ArticleUserInfo.as_view()),
]
urlpatterns = format_suffix_patterns(urlpatterns)
