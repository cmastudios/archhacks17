"""archhacks17 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout

from nutritrack import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^nutritrack/$', views.index, name='index'),
    url(r'^nutritrack/report/$', views.report, name='report'),
    url(r'^nutritrack/meals/$', views.meals, name='meals'),
    url(r'^nutritrack/eat/$', views.eat, name='eat'),
    url(r'^nutritrack/recipe/(?P<recipe_id>[0-9]+)/$', views.recipe, name='recipe'),
    url(r'^nutritrack/edamam/(?P<id>[0-9]+)/$', views.edamam, name='edamam'),
    url(r'^$', views.splash, name='splash'),
    url(r'^accounts/login/$', login, name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
    url(r'^accounts/profile/$', views.profile, name='profile'),
    url(r'^accounts/register/$', views.register, name='register')
]
