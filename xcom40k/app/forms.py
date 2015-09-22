from django import forms
from django.shortcuts import get_object_or_404

class YourNameForm(forms.Form):
	your_name = forms.CharField(label = 'Your name, please:', widget = forms.Textarea)

class UserEditForm(forms.Form):
	password_old = forms.CharField(label = 'old password', widget = forms.PasswordInput)
	password_new = forms.CharField(label = 'new password', widget = forms.PasswordInput)
	password_new_rpt = forms.CharField(label = 'repeat', widget = forms.PasswordInput)

class TokenBuyForm(forms.Form):
	count = forms.IntegerField(label = 'How many?', initial = 1)

class AbilityTrainForm(forms.Form):
	def __init__(self, class_ids, *args, **kwargs):
		super(AbilityTrainForm, self).__init__(*args, **kwargs)
		choices = Abilities.objects.filter(cls = class_id)
		self.fields['abilities'] = forms.MultipleChoiceField(label = 'Select abilities', choices = choices)