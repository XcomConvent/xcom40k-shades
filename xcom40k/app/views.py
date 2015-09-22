from functools import wraps
from django.shortcuts import render, get_object_or_404, redirect
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
from django.views.generic.edit import CreateView, UpdateView, ModelFormMixin

#from django.contrib.auth.decorators import login_required, user_passes_test

def login_required(func):
	@wraps(func)
	def wrap(*args, **kwargs):
		instance = args[0]
		request = args[1]
		if (request.user.is_authenticated()):
			return func(*args, **kwargs)
		return redirect(reverse('app:login'))
	return wrap

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
		return str(s) + (' ' * (count - len(s)))
	def d(self, data):
		self.logger.info    ('[' + self._str_complement('INFO', 8) + ' @ ' + str(timezone.now()) + '/' + BUILD_NAME + ' v' + str(BUILD_VERSION) + '] // ' 
			+ self._str_complement(str(self.comp), 10) + ' //: ' + str(data))
	def warn(self, data):
		self.logger.warning ('[' + self._str_complement('WARNING', 8) + ' @ ' + str(timezone.now()) + '/' + BUILD_NAME + ' v' + str(BUILD_VERSION) + '] // ' 
			+ self._str_complement(str(self.comp), 10) + ' //: ' + str(data))
	def shout(self, data):
		self.logger.critical('[' + self._str_complement('CRITICAL', 8) + ' @ ' + str(timezone.now()) + '/' + BUILD_NAME + ' v' + str(BUILD_VERSION) + '] // ' 
			+ self._str_complement(str(self.comp), 10) + ' //: ' + str(data))

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
	user = None
	def __str__(self):
		return self.TAG
	def __init__(self):
		self.Log = _Log(self.TAG)
			

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

			@login_required
			def view(self, request):
				related_chars = Char.objects.filter(host=request.user.pk)
				context = {'user': request.user, 'related_chars': related_chars}
				return my_render_wrapper(request, 'app/profile/users/view.html', context)
			
			@login_required
			def edit(self, request):
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
				context = {'user': request.user, 'char': char, 'items': request.user.account.items.all(), 'abilities': char.abilities.all(), }
				return my_render_wrapper(request, 'app/profile/chars/view.html', context)
			def edit(self, request, char_id):
				char = Char.objects.filter(pk = char_id)[0]
				context = {'user': request.user, 'char': char, 'items': request.user.account.items.all(), 'abilities': char.abilities.all(), }
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

			@login_required
			def index(self, request, mission_id):
				mis = get_object_or_404(Mission, pk = mission_id)
				chars = Char.objects.filter(host = request.user.pk)
				idlers = []
				for char in chars:
					if (char not in mis.participants.all()):
						idlers.append(char)
				context = {'mission': mis, 'chars': chars, 'idlers': idlers, 'parts': mis.participants.all()}
				return my_render_wrapper(request, 'app/missions/fly.html', context)
			
			@login_required
			def edit(self, request, mission_id, char_id):
				# todo: equipment-alter room 
				mis = get_object_or_404(Mission, pk = mission_id)
				char = get_object_or_404(Char, pk = char_id)
				mis.participants.add(char)
				mis.save()
				return HttpResponseRedirect(reverse('app:missions.view', args = (mission_id,)))
			
			@login_required
			def rm(self, request, mission_id, char_id):
				mis = get_object_or_404(Mission, pk = mission_id)
				char = get_object_or_404(Char, pk = char_id)
				if (char not in mis.participants.all()):
					raise HttpResponseBadRequest('Character #' + char.pk + ' is not participant of mission #' + mis.pk)
				mis.participants.remove(char)
				mis.save()
				return HttpResponseRedirect(reverse('app:missions.view', args = (mission_id,)))
		
		@login_required
		def pdf(self, request, mission_id):
			return HttpResponse('Pdf for mission #' + str(mission_id) + ' for user ' + request.user.username)

		@login_required
		def report(self, request, mission_id):
			return HttpResponseRedirect(reverse('app:profile.reports.new', args = (mission_id,)))

	class stash(SiteComponent):
		TAG = 'STASH'
		def _get_public_stash(self):
			root = get_object_or_404(User, username = 'root')
			public_stash = root.account.items.all()
			return public_stash

		def index(self, request):
			return HttpResponseRedirect(reverse('app:stash.view'))

		def view(self, request):
			context = {'tokens': self._get_public_stash(), }
			return my_render_wrapper(request, 'app/stash/view.html', context)

		class token(SiteComponent):
			TAG = 'STASH-BUY'
			def _transfer_it(self, source_user, item_token, qty, target_user):
				if source_user is target_user:
					return None
				if item_token.count == qty:
					item_token.delete()
				else:
					item_token.count -= qty
					item_token.save()
				these_item = target_user.account.items.filter(item = item_token.item)
				if len(these_item) == 0:
					target_user.account.items.create(item = item_token.item, count = qty)
				else:
					these_item[0].count += qty
					these_item[0].save()
				
				s = ''
				if source_user.username == 'root':
					s = 'Public Stash'
				else:
					s = source_user.username

				self.Log.d('[' + s + '] -> [' + target_user.username + '], item ' + str(item_token.item) + ' x' + str(qty) + '.')
				return None

			@login_required
			def buy(self, request, token_id):				
				it = get_object_or_404(ItemToken, pk = token_id)
				if request.method == 'GET':
					return my_render_wrapper(request, 'app/stash/token_view.html', {'form': TokenBuyForm(), 'it': it})	
				elif request.method == 'POST':
					form = TokenBuyForm(request.POST)
					if form.is_valid() and form.cleaned_data['count'] <= it.count:
						self._transfer_it(get_object_or_404(User, username = 'root'), it, form.cleaned_data['count'], request.user)
						return HttpResponseRedirect(reverse('app:stash.view'))
					else:
						return HttpResponseRedirect(reverse('app:stash.tokens.buy', args = (token_id,)))
				else:
					raise HttpResponseBadRequest('Invalid method, expected GET/POST, found ' + request.method)
		
		class sell(SiteComponent):
			TAG = 'STASH-SELL'

			@login_required
			def add(self, request):
				return HttpResponse('Add a token for selling')

			@login_required
			def make(self, request):
				return HttpResponseRedirect(reverse('app:stash.view'))

	class train(SiteComponent):
		TAG = 'TRAIN'
		
		@login_required
		def index(self, request):
			charnames = map(str, Char.objects.filter(host = request.user.pk))
			abilities = {}
			for charname in charnames:
				temp = map(str, Ability.objects.all())
				temp = tuple(temp)
				for aby in temp:
					print aby
				abilities.update({charname: temp})
			context = {'charnames': charnames, 'abilities': abilities}

			return my_render_wrapper(request, 'app/train/index.html', context)

		@login_required
		def edit(self, request, char_id):			
			if request.method == 'GET':
				char = get_object_or_404(Char, pk = char_id)
				class_level_pairs = char.classes.all()
				for clp in class_level_pairs:
					print (clp.cls + ' of level ' + clp.level)
				return HttpResponse('Everything is OK')
#				return my_render_wrapper(request, 'app/train/edit.html', context)	
			elif request.method == 'POST':
				form = AbilityTrainForm(request.POST)
				if form.is_valid():
					return HttpResponse('Everything is OK')
				else:
					return HttpResponseRedirect(reverse('app:train.edit'))
			else:
				raise HttpResponseBadRequest('Invalid method, expected GET/POST, found ' + request.method)		
		class neuro(SiteComponent):
			TAG = 'NEURO'

			@login_required
			def index(self, request):
				nrequests = NeuroRequest.objects.filter(status = 0)
				context = {'nrequests': nrequests}
				return my_render_wrapper(request, 'app/train/neuro.html', context)

			class NeuroRequestCreateViewGeneric(CreateView):
				model = NeuroRequest
				fields =  ['teacher', 'pupil', 'target_class',]
				template_name = 'app/train/neuro_add.html'
				#url = reverse('app:train.neuro')
				def form_valid(self, form):
					self.object = form.save(commit = False)
					self.object.pub_date = timezone.now()
					self.object.save()
					return super(ModelFormMixin, self).form_valid(form)
				def get_success_url(self):
					return reverse('app:train.neuro')
#			def add(self, request):
#				return site().train().neuro().NeuroRequestCreateViewGeneric.as_view(request)	
	class nfo(SiteComponent):
		TAG = 'NFO'
		def storyline(self, request):
			return HttpResponse('Our heroic storyline')
		def rnd(self, request):
			return HttpResponseRedirect('wiki/')
		def recruit(self, request):
			return HttpResponseRedirect('wiki/Recruitment.html')


