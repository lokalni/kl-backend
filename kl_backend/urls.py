"""kl_backend URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from kl_participants import views as participants_views
from kl_conferences import views as conference_views
from kl_backend import views as backend_views

router = DefaultRouter()
router.register(r'students', participants_views.StudentViewSet, basename='students')
router.register(r'groups', participants_views.GroupViewSet, basename='groups')
router.register(r'rooms', conference_views.RoomViewSet, basename='rooms')
router.register(r'nodes', conference_views.ServerNodeSelfServiceViewSet, basename='nodes')
router.register(r'accounts', backend_views.AccountsViewSet, basename='accounts')
urlpatterns = router.urls

root_urlpatterns = [
    path('<str:token>', lambda r, token: HttpResponseRedirect(f'/api/v1/rooms/join/{token}')),
    path('admin/', admin.site.urls),
    path(r'l/<str:token>', participants_views.quick_login),
]


urlpatterns = [url(r'^api/v1/', include(router.urls))] + root_urlpatterns
