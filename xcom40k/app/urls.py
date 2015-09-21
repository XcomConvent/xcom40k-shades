from . import views
from django.conf.urls import include, url

urlpatterns = [
	# index page
	url(r'^$', views.site().index, name = 'index'),
    
    # login form
    url(r'^login/$', views.site().login, name = 'login'),
    url(r'^logout/$', views.site().logout, name = 'logout'),
    
    # testing form
    url(r'^your-name/$', views.site().yourname, name = 'yourname'),

    # profiles
    url(r'^profile/$', views.site().profile().index, name = 'profile'),
    ## reports 
    url(r'^profile/reports/$', views.site().profile().reports().index, name = 'profile.reports'),
    url(r'^profile/reports/(?P<report_id>)/view/$', views.site().profile().reports().view, name = 'profile.reports.view'),
    url(r'^profile/reports/(?P<report_id>)/edit/$', views.site().profile().reports().edit, name = 'profile.reports.edit'),
#    url(r'^profile/reports/(?P<report_id>)/pdf/$', views.site().profile().reports().pdf, name = 'profile.reports.pdf'),
    ## users
    url(r'^profile/users/view/$', views.site().profile().users().view, name = 'profile.users.view'),
    url(r'^profile/users/edit/$', views.site().profile().users().edit, name = 'profile.users.edit'),
    ## chars
    url(r'^profile/chars/new/$', views.site().profile().chars().new, name = 'profile.chars.new'),
    url(r'^profile/chars/(?P<char_id>[0-9]+)/view/$', views.site().profile().chars().view, name = 'profile.chars.view'),
	url(r'^profile/chars/(?P<char_id>[0-9]+)/edit/$', views.site().profile().chars().edit, name = 'profile.chars.edit'),

    # missions
    url(r'^missions/$', views.site().missions().index, name = 'missions'),
    url(r'^missions/(?P<mission_id>[0-9]+)/view/$', views.site().missions().fly().index, name = 'missions.view'),
    url(r'^missions/(?P<mission_id>[0-9]+)/(?P<char_id>[0-9]+)/edit/$', views.site().missions().fly().edit, name = 'missions.edit'),
    url(r'^missions/(?P<mission_id>[0-9]+)/pdf/$', views.site().missions().pdf, name = 'missions.pdf'),
    url(r'^missions/(?P<mission_id>[0-9]+)/(?P<char_id>[0-9]+)/rm/$', views.site().missions().fly().rm, name = 'missions.rm'),
	url(r'^missions/(?P<mission_id>[0-9]+)/report/$', views.site().missions().report, name = 'missions.report'),

    # stash
    url(r'^stash/$', views.site().stash().index, name = 'stash'),
    url(r'^stash/view/$', views.site().stash().view, name = 'stash.view'),
    url(r'^stash/(?P<item_token_id>[0-9]+)/buy/$', views.site().stash().token().buy, name = 'stash.tokens.buy'),
    url(r'^stash/sell/add/$', views.site().stash().sell().add, name = 'stash.sell.add'),
    url(r'^stash/sell/make/$', views.site().stash().sell().make, name = 'stash.sell.make'),

    # train 
    url(r'^train/$', views.site().train().index, name = 'train'),
    url(r'^train/(?P<char_id>[0-9]+)/edit/$', views.site().train().edit, name = 'train.edit'),
    url(r'^train/neuro/$', views.site().train().neuro().index, name = 'train.neuro'),
    url(r'^train/neuro/add/$', views.site().train().neuro().add, name = 'train.neuro.add'),

    # rnd & stuff
    url(r'^rnd/storyline/$', views.site().nfo().storyline, name = 'nfo.storyline'),
    url(r'^rnd/rnd/$', views.site().nfo().rnd, name = 'nfo.rnd'), # wiki engine? Markdoc
    url(r'^rnd/recruit/$', views.site().nfo().recruit, name = 'nfo.recruit'),
]
