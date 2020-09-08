"""jobs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from accounts.views import (UserInfoView,)

# def sredirect(request, url):
#     return HttpResponseRedirect("/#/%s" % url)


# def app(request):
#     return render(request, 'index.html')

urlpatterns = [
    re_path(r'^api/auth-jwt', obtain_jwt_token),
    re_path(r'^api/auth-jwt-refresh', refresh_jwt_token),
    re_path(r'^api/auth-jwt-verify', verify_jwt_token),

    path('admin/', admin.site.urls),
    path('api/user/info', UserInfoView.as_view(), name='user'),

    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('main.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)


urlpatterns += [
    # JS-приложение
    # url(r'^$', app, name='app'),
    # url(r'^(?P<url>.*)$', sredirect),
]
