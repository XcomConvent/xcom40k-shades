from . import views
from django.conf.urls import include, url

urlpatterns = [
	url(r'^missions/changestate/(?P<mission_id>[0-9]+)/(?P<new_state>[0-9]+)/$', views.mission_changestate, name = 'missions.changestate'),
]