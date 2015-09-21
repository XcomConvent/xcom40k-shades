from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.core.urlresolvers import reverse
from django.views import generic
from django.contrib.auth import views, logout
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
import logging
from django.utils import timezone
from .forms import *
from .models import *
from xcom40k.settings import BUILD_NAME, BUILD_VERSION

''' LOGGING
	Logging is declared and initialized here.

	Look at settings.py for config.
	Look at docs/logging for logging policy.
'''
class _Log:
	logger = None
	comp = None
	def __init__(self, TAG):
		self.logger = logging.getLogger('xcom40k.high')
		self.comp = TAG
	def _str_complement(self, s, count):
		return s + (' ' * (count - len(s)))
	def d(self, data):
		self.logger.info    ('[' + self._str_complement('INFO', 8) + ' @ ' + str(timezone.now()) + '/' + BUILD_NAME + ' v' + BUILD_VERSION + '] // ' 
			+ self._str_complement(str(self.comp), 10) + ' //: ' + data)
	def warn(self, data):
		self.logger.warning ('[' + self._str_complement('WARNING', 8) + ' @ ' + str(timezone.now()) + '/' + BUILD_NAME + '] // ' 
			+ self._str_complement(str(self.comp), 10) + ' //: ' + data)
	def shout(self, data):
		self.logger.critical('[' + self._str_complement('CRITICAL', 8) + ' @ ' + str(timezone.now()) + '/' + BUILD_NAME + '] // ' 
			+ self._str_complement(str(self.comp), 10) + ' //: ' + data)

''' SITE COMPONENTS
	The list of site's components is here for listing in sidemenu.
	
	Look at docs/sitemap for further information.
'''
class SiteComponentUrl:
	name = ''
	url = ''
	def __str__(self):
		return self.name
	def mk(self, name, url):
		s = SiteComponentUrl()
		s.name = name
		s.url = url
		return s

def get_component_list():
	return (
		SiteComponentUrl().mk(name = 'Profiles',  url = 'profile'),
		SiteComponentUrl().mk(name = 'Missions',  url = 'missions'),
		SiteComponentUrl().mk(name = 'Stash',     url = 'stash'),
		SiteComponentUrl().mk(name = 'Training',  url = 'train'),
	)

def get_global_context(request):
	return {'list_components': get_component_list(), 'user': request.user}

def my_render_wrapper(request, template, context):
	context.update(get_global_context(request))
	return render(request, template, context)

class SiteComponent:
	TAG = 'UNKNOWN'
	Log = None
	def __str__(self):
		return self.TAG
	def __init__(self):
		self.Log = _Log(self.TAG)
	def auth(self, request):
		if request.user is not None and request.user.username != '':
			# the password verified for the user
			if request.user.is_active:
				return (0, 'OK')
			else:
				self.Log.d('An inactive user #' + str(request.user.pk) + ' named ' + str(request.user.username) + ' tried to enter but was denied.')
				return (2, 'Your account has been disabled')
		else:
			return (1, 'Authentication failed')

''' VIEWS
	Views are implemented here
	
	Look at docs/component/<component_name> for further information.
	<component_name> equals TAG in each class and subclass.
'''
class site(SiteComponent):
	TAG = 'MAIN'

	def index(self, request):
		context = {'list_components': get_component_list()}
		return my_render_wrapper(request, 'app/index.html', context)

	def login(self, request):
		template_response = views.login(request, template_name = 'app/auth/login.html')
		return template_response

	def logout(self, request):
		views.logout(request)
		return HttpResponseRedirect(reverse('app:index'))

	# test component
	# subjected to remove
	def yourname(self, request):
		Log.warn('user ' + request.user.username + ' is using app.yourname component')
		if request.method == 'POST':
			form = YourNameForm(request.POST)
			if form.is_valid():
				return HttpResponseRedirect('thanks/')
		else:
			form = YourNameForm()
			return my_render_wrapper(request, 'app/yourname.html', {'form': form})
	# end of test component

	class profile(SiteComponent):
		TAG = 'PROFILE'

		def index(self, request):
#			self.Log.d('user "' + str(request.user.username) + '" views his profile')
			return HttpResponseRedirect(reverse('app:profile.users.view'))

		class users(SiteComponent):
			TAG = 'USERS'

			def view(self, request):
				code = self.auth(request)
				if code[0] == 2:
					return HttpResponseForbidden(code[1])
				if code[0] == 1:
					return HttpResponseRedirect(reverse('app:login'))

				related_chars = Char.objects.filter(host=request.user.pk)
				context = {'user': request.user, 'related_chars': related_chars}
				return my_render_wrapper(request, 'app/profile/users/view.html', context)
			
			def edit(self, request):
				code = self.auth(request)
				if code[0] == 2:
					return HttpResponseForbidden(code[1])
				if code[0] == 1:
					return HttpResponseRedirect(reverse('app:login'))
				
				if request.method == 'GET':
					return my_render_wrapper(request, 'app/profile/users/edit.html', {'form': UserEditForm()})	
				elif request.method == 'POST':
					form = UserEditForm(request.POST)
					if form.is_valid() and form.cleaned_data['password_new'] == form.cleaned_data['password_new_rpt']:
						u = get_object_or_404(User, pk = request.user.pk)
						u.set_password(form.cleaned_data['password_new'])
						u.save()
						return HttpResponseRedirect(reverse('app:profile.users.view',))
					else:
						return HttpResponseRedirect(reverse('app:profile.users.edit',))
				else:
					raise HttpResponseBadRequest('Invalid method, expected GET/POST, found ' + request.method)

		class chars(SiteComponent):
			TAG = 'CHARS'
			def view(self, request, char_id):
				char = Char.objects.filter(pk = char_id)[0]
				context = {'user': request.user, 'char': char, 'items': char.items.all(), 'abilities': char.abilities.all(), }
				return my_render_wrapper(request, 'app/profile/chars/view.html', context)
			def edit(self, request, char_id):
				char = Char.objects.filter(pk = char_id)[0]
				context = {'user': request.user, 'char': char, 'items': char.items.all(), 'abilities': char.abilities.all(), }
				return my_render_wrapper(request, 'app/profile/chars/edit.html', context)
			def new(self, request):
				# ...
				self.Log.d('User ' + request.user.username + ' has created new character named ')
				return HttpResponseRedirect(reverse('app:profile.chars.view', args = (char_id,)))

		class reports(SiteComponent):
			TAG = 'REPORTS'
			def index(self, request):
				return HttpResponse('Index of reports page')
			def view(self, request, report_id):
				return HttpResponse('View report #' + str(report_id))
			def edit(self, request, user_id, char_id):
				return HttpResponse('Edit report #' + str(report_id))
			def save(self, request, user_id, char_id):
				return HttpResponseRedirect(reverse('app:profile.reports.view', args = (str(report_id),)))

	class missions(SiteComponent):
		TAG = 'MISSIONS'
		def index(self, request):
			ms = Mission.objects.all()
			context = {'missions': ms}
			return my_render_wrapper(request, 'app/missions/index.html', context)
		class fly(SiteComponent):
			TAG = 'FLY'
			def index(self, request, mission_id):
				code = self.auth(request)
				if code[0] == 2:
					return HttpResponseForbidden(code[1])
				if code[0] == 1:
					return HttpResponseRedirect(reverse('app:login'))
				mis = get_object_or_404(Mission, pk = mission_id)
				chars = Char.objects.filter(host = request.user.pk)
				idlers = Char.objects.filter(host = request.user.pk)
				for char in chars:
					if (char in mis.participants.all()):
						idlers.remove(char)
				context = {'mission': mis, 'chars': chars, 'idlers': idlers, 'parts': mis.participants.all()}
				return my_render_wrapper(request, 'app/missions/fly.html', context)
			def edit(self, request, mission_id, char_id):
				# todo: equipment-alter room 
				return HttpResponseRedirect(reverse('app:missions.view', args = (mission_id,)))
			def rm(self, request, mission_id, char_id):
				code = self.auth(request)
				if code[0] == 2:
					return HttpResponseForbidden(code[1])
				if code[0] == 1:
					return HttpResponseRedirect(reverse('app:login'))
				mis = get_object_or_404(Mission, pk = mission_id)
				char = get_object_or_404(Char, pk = char_id)
				if (char not in mis.participants.all()):
					raise HttpResponseBadRequest('Character #' + char.pk + ' is not participant of mission #' + mis.pk)
				mis.participants.remove(char)
				mis.save()
				return HttpResponseRedirect(reverse('app:missions.view', args = (mission_id,)))

		def pdf(self, request, mission_id):
			return HttpResponse('Pdf for mission #' + str(mission_id) + ' for user ' + request.user.username)
		def report(self, request, mission_id):
			return HttpResponseRedirect(reverse('app:profile.reports.new', args = (mission_id,)))

	class stash(SiteComponent):
		TAG = 'STASH'
		def index(self, request):
			return HttpResponseRedirect(reverse('app:stash.view'))
		def view(self, request):
			return HttpResponse('View stash tokens')
		class token(SiteComponent):
			TAG = 'STASH-BUY'
			def buy(self, request, token_id):
				return HttpResponse('Try to buy token #' + str(token_id))
		class sell(SiteComponent):
			TAG = 'STASH-SELL'
			def __str__(self):
				return 'STASH-SELL'
			def add(self, request):
				return HttpResponse('Add a token for selling')
			def make(self, request):
				return HttpResponseRedirect(reverse('app:stash.view'))

	class train(SiteComponent):
		TAG = 'TRAIN'
		def index(self, request):
			return HttpResponse('Index of training grounds')
		def edit(self, request, char_id):
			return HttpResponse('Edit skills of char_id')
		def save(self, request, char_id):
			return HttpResponseRedirect(reverse('app:train'))
		class neuro(SiteComponent):
			TAG = 'NEURO'
			def index(self, request):
				return HttpResponse('Index of neurotrainer')
			def add(self, request):
				return HttpResponse('Add a neurotrainer request')
			def save(self, request):
				return HttpResponseRedirect(reverse('app:train.neuro'))
	
	class nfo(SiteComponent):
		TAG = 'NFO'
		def storyline(self, request):
			return HttpResponse('Our heroic storyline')
		def rnd(self, request):
			return HttpResponseRedirect('wiki/')
		def recruit(self, request):
			return HttpResponseRedirect('wiki/Recruitment.html')
