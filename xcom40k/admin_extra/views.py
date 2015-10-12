from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseServerError
from django import forms
from app.models import * 
from app.views import my_render_wrapper, site
from django.contrib.contenttypes.models import ContentType
from django.contrib import admin
from django.utils import timezone

class MissionFinalizeForm(forms.Form):
	def __init__(self, mission_id, *args, **kwargs):
		super(MissionFinalizeForm, self).__init__(*args, **kwargs)
		participants = get_object_or_404(Mission, pk = mission_id).participants.all()
		for char in participants:
			self.fields['character_' + str(char.pk)] = forms.IntegerField(label = char.name)
	text = forms.CharField(max_length = 10000)

class nameurlpair:
	name = ''
	url = ''
	def __init__(self, name, url):
		self.name = name
		self.url = url

def mission_changestate(request, mission_id, new_state):
	if int(new_state) < 3:
		mis = get_object_or_404(Mission, pk = mission_id)
		mis.status = new_state
		mis.save()
		return HttpResponseRedirect('/admin/app/missions/') # TODO 
	else:
		return mission_finalize(request, mission_id)

def mission_finalize(request, mission_id):
	if request.method == 'GET':
		participants = get_object_or_404(Mission, pk = mission_id).participants.all()
		nup = []
		for char in participants:
			rrr = Report.objects.filter(related_char = char.pk, related_mission = mission_id)
			if (len(rrr) > 0):
				report_id = rrr[0].pk
				url_report = reverse('app:profile.reports.view', args = (report_id,))
				nup.append(nameurlpair(name=char.name, url=url_report))
		context = {'form': MissionFinalizeForm(mission_id), 'nup': nup}
		return my_render_wrapper(request, 'admin_extra/missions_finalize.html', context)
	elif request.method == 'POST':
		form = MissionFinalizeForm(mission_id, request.POST)
		participants = get_object_or_404(Mission, pk = mission_id).participants.all()
		if form.is_valid():
			rewards = []
			for char in participants:
				exp = form.cleaned_data['character_' + str(char.pk)]
				rewards.append((char.pk, exp,))
			site().train()._add_exp_bulk(mission_id, rewards)
			text = form.cleaned_data['text']
			text = '...' # TODO form a post
			#BlogEntry.create(author = get_object_or_404(Account, pk = request.user.pk), text = text, pub_date = timezone.now())
			return HttpResponseRedirect(reverse('admin:index'))
