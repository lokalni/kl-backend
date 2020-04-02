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
from django.contrib import admin
from django.urls import path, re_path
from django.conf import settings
from rest_framework.routers import DefaultRouter

from kl_participants.views import *
from kl_conferences.views import *

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='students')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'rooms', RoomViewSet, basename='rooms')
router.register(r'nodes', ServerNodeSelfServiceViewSet, basename='nodes')
urlpatterns = router.urls


# FIXME
from django.conf.urls.static import static

urlpatterns = [
    # FIXME lame AF
    path('', lambda r: HttpResponseRedirect('/static/index.html')),
    re_path(r'^(?P<req_path>(js|css|img|favicon.ico)/.*)$', lambda r, req_path: HttpResponseRedirect(f'/static/{req_path}')),

    path('<str:token>', lambda r, token: HttpResponseRedirect(f'/rooms/join/{token}')),
    path('admin/', admin.site.urls),
    path(r'l/<str:token>', quick_login)
] + router.urls + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
