from django import forms

class YourNameForm(forms.Form):
	your_name = forms.CharField(label = 'Your name, please:', widget = forms.Textarea)

class UserEditForm(forms.Form):
	password_old = forms.CharField(label = 'old password', widget = forms.PasswordInput)
	password_new = forms.CharField(label = 'new password', widget = forms.PasswordInput)
	password_new_rpt = forms.CharField(label = 'repeat', widget = forms.PasswordInput)
