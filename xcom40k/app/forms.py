from django import forms
from django.shortcuts import get_object_or_404
from .models import *

class YourNameForm(forms.Form):
	your_name = forms.CharField(label = 'Your name, please:', widget = forms.Textarea)

class UserEditForm(forms.Form):
	password_old = forms.CharField    (label = 'old password', widget = forms.PasswordInput)
	password_new = forms.CharField    (label = 'new password', widget = forms.PasswordInput)
	password_new_rpt = forms.CharField(label = 'repeat',       widget = forms.PasswordInput)

class TokenBuyForm(forms.Form):
	count = forms.IntegerField(label = 'How many?', initial = 1)

class AbilityTrainForm(forms.Form):
	def __init__(self, *args, **kwargs):
		class_ids = kwargs.pop('class_ids', None)
		char_id = kwargs.pop('char_id', None)
		super(AbilityTrainForm, self).__init__(*args, **kwargs)
		if not self.is_bound:
			char = get_object_or_404(Char, pk = char_id)
			for class_id in class_ids:
				cls = get_object_or_404(Class, pk = class_id)
				abilities = Ability.objects.filter(cls = class_id)

				choices = [(ab.pk, '({0}) {2}xp: {1}'.format(str(ab.cls), str(ab), str(ab.exp_cost))) for ab in abilities]

				already_taken = []
				for ab in char.abilities.all():
					if ab in abilities:
						already_taken.append(ab.pk)
				self.fields['abilities_cl{}'.format(str(class_id))] = forms.MultipleChoiceField(label = 'Select abilities for {} class'.format(str(cls)), choices = choices, initial = already_taken, widget = forms.CheckboxSelectMultiple)
	def parse(self, data):
		lists = data.lists()
		cleaned = {}
		for item in lists:
			if item[0] != u'csrfmiddlewaretoken':
				ab_list = []
				for ab_id in item[1]:
					ab_list.append(get_object_or_404(Ability, pk = int(ab_id)))
			cleaned.update({str(item[0]): ab_list})
		return cleaned