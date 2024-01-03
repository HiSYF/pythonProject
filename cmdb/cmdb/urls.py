"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from user.MyObtainTokenPairView import MyObtainTokenPairView
from rest_framework.routers import DefaultRouter
from django.views.generic import TemplateView
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('',TemplateView.as_view(template_name='index.html')),

    # path('api/token/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),  # 自定义token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/user/info/',user/info/.as_view()),
    # path('api/', include('devops.urls')),  # 包含其它页面的路由地址
    path('api/', include('devops.urls')), #包含其它页面的路由地址
    path('api/', include('user.urls')),  # 包含其它页面的路由地址
    path('api/', include('lmt.urls')), # liumeiti
    path('api/', include('jenkinsJob.urls')),  # jenkinsJob

    path('api/', include('webssh.urls')),  # webssh,远程服务器日志

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)