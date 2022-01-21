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
from django.conf.urls import url
from . import views

urlpatterns = [
    # http://localhost:8000/generatescenario/
    url(r'^$', views.index, name='index'),
    #url('scenario_gen', views.scenario_gen, name='scenario_gen'),
    url(r'^scenario_gen/$', views.scenario_gen, name='scenario_gen'),
    url(r'^scenario_api/$', views.scenario_api, name='scenario_api'),

    # http://localhost:8000/scenario/754 or http://localhost:8000/scenario/754/
    #url(r'^(?P<seed_value>[0-9]+)$', views.specific_scenario, name='specific_scenario'),
    #url(r'^(?P<seed_value>[0-9]+)/$', views.specific_scenario, name='specific_scenario'),
]