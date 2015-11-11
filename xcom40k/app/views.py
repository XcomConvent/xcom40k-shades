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
from django.forms import formset_factory
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
		print ('[' + self._str_complement('INFO', 8) + ' @ ' + str(timezone.now()) + '/' + BUILD_NAME + ' v' + str(BUILD_VERSION) + '] // ' 
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

	''' blog entries
	'''
	def index(self, request):
		be = BlogEntry.objects.all()
		context = {'list_components': get_component_list(), 'blog_entries': be}
		return my_render_wrapper(request, 'app/mainpage.html', context)
	''' auth 
	'''
	def login(self, request):
		template_response = views.login(request, template_name = 'app/auth/login.html')
		return template_response
	''' logout -> index
	'''
	def logout(self, request):
		views.logout(request)
		return HttpResponseRedirect(reverse('app:index'))

	class profile(SiteComponent):
		TAG = 'PROFILE'

		@login_required
		def index(self, request):
#			self.Log.d('user "' + str(request.user.username) + '" views his profile')
			return HttpResponseRedirect(reverse('app:profile.users.view', args = (request.user.pk,)))

		class users(SiteComponent):
			TAG = 'USERS'

			def view(self, request, user_id):
				user = get_object_or_404(User, pk = user_id)
				related_chars = Char.objects.filter(host = user.pk)
				context = {'target_user': user, 'related_chars': related_chars}
				return my_render_wrapper(request, 'app/profile/users/view.html', context)
			
			@login_required
			def edit(self, request, user_id):
				if request.method == 'GET':
					target_user = get_object_or_404(User, pk = user_id)
					if (target_user.pk != request.user.pk):
						return HttpResponseForbidden("Are you root?")
					return my_render_wrapper(request, 'app/profile/users/edit.html', {'form': UserEditForm(), 'target_user': target_user})	
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
			ms = Mission.objects.filter(status__lte = 2)
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
			public_stash = ItemMarketToken.objects.all()
			return public_stash

		def index(self, request):
			return HttpResponseRedirect(reverse('app:stash.view'))

		def view(self, request):
			context = {'tokens': self._get_public_stash(), }
			return my_render_wrapper(request, 'app/stash/view.html', context)

		class token(SiteComponent):
			TAG = 'STASH-BUY'
			def _transfer_it(self, source_user, item_token, qty, target_user):
				if source_user.pk == target_user.pk:
					return None
				if item_token.count == qty:
					item_token.delete()
				else:
					item_token.count -= qty
					item_token.save()
				these_item = target_user.account.items.filter(item = item_token.item)
				if len(these_item) == 0:
					newtoken = ItemToken.objects.create(item = item_token.item, count = qty)
					newtoken.save()
					target_user.account.items.add(newtoken)
				else:
					these_item[0].count += qty
					these_item[0].save()
				target_user.save()
				self.Log.d('[' + source_user.user.username + '] -> [' + target_user.username + '], item ' + str(item_token.item) + ' x' + str(qty) + '.')
				return None

			@login_required
			def buy(self, request, market_token_id):				
				imt = get_object_or_404(ItemMarketToken, pk = market_token_id)
				your_money = request.user.account.money
				if request.method == 'GET':
					return my_render_wrapper(request, 'app/stash/token_view.html', {'form': TokenBuyForm(), 'imt': imt})	
				elif request.method == 'POST':
					form = TokenBuyForm(request.POST)
					if form.is_valid() and int(form.cleaned_data['count']) <= int(imt.item_token.count) and int(your_money) >= int(form.cleaned_data['count']) * int(imt.item_token.price):
 						# money reduction
						acc = request.user.account
						acc.money -= form.cleaned_data['count']* imt.item_token.price
						acc.save()
						# item transfer
						self._transfer_it(imt.owner, imt.item_token, form.cleaned_data['count'], request.user)

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

		def _add_exp_money_bulk(self, mission_id, rewards, money):
			for reward in rewards:
				target_pk = reward[0]
				target_exp  = reward[1]
				
				target_char = get_object_or_404(Char.objects.filter(pk = target_pk))
				target_char.exp += target_exp
				target_char.save()

				target_user = target_char.host
				target_user.account.money += money
				target_user.account.save()
			pass

		@login_required
		def index(self, request):
			chars = Char.objects.filter(host = request.user.pk)
			abilities = {}
			for char in chars:
				abilities.update({char.name: char.abilities.all()})
			context = {'chars': chars, 'abilities': abilities}

			return my_render_wrapper(request, 'app/train/index.html', context)

		@login_required
		def edit(self, request, char_id):			
			char = get_object_or_404(Char, pk = char_id)
			if request.method == 'GET':
				class_level_pairs = char.classes.all()
				class_ids = []
				for clp in class_level_pairs:
					class_ids.append(clp.cls.pk)
				context = {'char': char, 'form': AbilityTrainForm(class_ids = class_ids, char_id = char_id)}
				
				return my_render_wrapper(request, 'app/train/edit.html', context)	
			elif request.method == 'POST':
				form = AbilityTrainForm(request.POST)
				if form.is_valid():
					totalxpcost = 0
					cleaned_data = form.parse(request.POST)
					for clp in char.classes.all():
						if 'abilities_cl{}'.format(str(clp.cls.pk)) in cleaned_data:
							for ab in cleaned_data['abilities_cl{}'.format(clp.cls.pk)]:
								if (ab not in char.abilities.all()):
									totalxpcost += ab.exp_cost
									char.abilities.add(ab)
					char.exp -= totalxpcost
					char.save()
					return HttpResponseRedirect(reverse('app:train'))
				else:
					return HttpResponseRedirect(reverse('app:train.edit'))
			else:
				raise HttpResponseBadRequest('Invalid method, expected GET/POST, found ' + request.method)		

		class neuro(SiteComponent):
			TAG = 'NEURO'

			@login_required
			def index(self, request):
				nrequests = NeuroRequest.objects.filter(status = 0)
				can_authorize = True
				context = {'nrequests': nrequests, 'can_authorize': can_authorize}
				return my_render_wrapper(request, 'app/train/neuro.html', context)
			def auth(self, request, nrq_id):
				nrq = get_object_or_404(NeuroRequest, pk = nrq_id)
				print(nrq.pupil, nrq.pupil.classes.all())
				level = 0
				if (len(nrq.pupil.classes.filter(cls = nrq.target_class)) != 0):
					level = nrq.pupil.classes.filter(cls = nrq.target_class)[0].level
					nrq.pupil.classes.filter(cls = nrq.target_class).delete()
				new_clp = ClassLevelPair(cls = nrq.target_class, level = level + 1)
				new_clp.save()
				nrq.pupil.classes.add(new_clp)
				
				nrq.status = 1
				nrq.closed_date = timezone.now()
				nrq.save()
				
				self.Log.d('Nrq id ' + str(nrq.pk) + ' from {} to {} by {} authorized '.format(nrq.teacher, nrq.pupil, nrq.target_class))
				return HttpResponseRedirect(reverse('app:train.neuro')) # I AM HERE

			class NeuroRequestCreateViewGeneric(CreateView):
				model = NeuroRequest
				fields =  ['teacher', 'pupil', 'target_class',]
				template_name = 'app/train/neuro_add.html'
				#url = reverse('app:train.neuro')
				def form_valid(self, form):
					self.object = form.save(commit = False)
					self.object.pub_date = timezone.now()
					self.object.closed_date = timezone.now()
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


