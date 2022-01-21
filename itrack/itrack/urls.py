"""itrack URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView
import scenario.views
import itrack.views

urlpatterns = [
    url(r'^admin', admin.site.urls),
    url(r'^admin/', admin.site.urls),
    #url(r'^', include('generatescenario.urls')),  # NOTE: without $
    url(r'^scenario', include('scenario.urls')),
    url(r'^scenario/', include('scenario.urls')),
    url(r'^scenario_api', scenario.views.scenario_api, name='scenario_api'),
    url(r'^scenario_api/', scenario.views.scenario_api, name='scenario_api'),
    url(r'^scenario_gen', scenario.views.scenario_gen, name='scenario_gen'),
    url(r'^scenario_gen/', scenario.views.scenario_gen, name='scenario_gen'),
    url(r'^$', itrack.views.index, name='index'),
    url(r'^docs/', itrack.views.index, name='index'),
    #url(r'^', RedirectView.as_view(url='http://127.0.0.1')),
    #url(r'^$', include('scenario.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
