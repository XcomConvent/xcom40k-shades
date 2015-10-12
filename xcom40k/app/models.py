from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse, HttpResponseRedirect

class CommonToken(models.Model):
	name = models.CharField(max_length=100)
	def __str__(self):
		return self.name
#	def get_admin_url(self):
#		content_type = ContentType.objects.get_for_model(self.__class__)
#		return reverse('admin:%s_%s_index' % (content_type.app_label, content_type.model))
#		return HttpResponseRedirect('admin/app/')
	class Meta:
		abstract = True

class Class(CommonToken):
	pass

class Ability(CommonToken):
	desc = models.CharField(max_length=2000, default = '')
	cls = models.ForeignKey(Class, default = None)
	required_level = models.PositiveIntegerField()
	exp_cost = models.PositiveIntegerField(default = 0)
	def get_abilities_filter(self, filtr):
		return eval('Ability.objects.filter(' + str(filtr) + ')')

class Item(CommonToken):
	SLOTS = (
		('s', 'Default Small Slot'),
		('l', 'Default Large Slot'),
	)
	desc = models.CharField(max_length=2000, default = '')
	slot = models.CharField(max_length=1, choices = SLOTS)

class ItemToken(models.Model):
	item = models.ForeignKey(Item)
	count = models.PositiveIntegerField()
	price = models.PositiveIntegerField(default=0)
	available = models.BooleanField(default=True)
	def __str__(self):
		return self.item.name + ' x' + str(self.count)

# we strongly recommend you not use Account model; 
# use django.contrib.auth.User model instead in any occurence you don't know which to choose.
class Account(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	items = models.ManyToManyField(ItemToken, blank = True)
	money = models.PositiveIntegerField(default = 0)

class ClassLevelPair(models.Model):
	cls = models.ForeignKey(Class)
	level = models.PositiveIntegerField(default = 0)
	def __str__(self):
		return str(self.cls) + ' ' + str(self.level) + 'lvl'

class Char(CommonToken):
	host = models.ForeignKey(User)
	classes = models.ManyToManyField(ClassLevelPair)
	abilities = models.ManyToManyField(Ability, blank = True)
	exp = models.PositiveIntegerField(default = 0)
	def class_level_pairs(self):
		s = ''
		for clp in self.classes.all():
			s += str(clp.cls) + ' lvl ' + str(clp.level) + ', '
		return s

class Mission(CommonToken):
	MISSION_STATUS = (
		(0, 'Not opened'),
		(1, 'Opened'),
		(2, 'Closed'),
		(3, 'Finalized'),
	)
	participants = models.ManyToManyField(Char)
	pub_date = models.DateField()
	finalize_date = models.DateField()
	status = models.PositiveIntegerField(choices = MISSION_STATUS, default = 0)
	def show_finalize_button(self):
		s = ''
		if self.status < 1:
			s = '<a href = "' + reverse('admin_extra:missions.changestate', args = (self.pk, 1)) + '"> Open </a>'
		elif self.status < 2:
			s = '<a href = "' + reverse('admin_extra:missions.changestate', args = (self.pk, 2)) + '"> Close </a>'
		elif self.status < 3:
			s = '<a href = "' + reverse('admin_extra:missions.changestate', args = (self.pk, 3)) + '"> Finalize </a>'
		else:
			s = 'Finalized on ' + str(self.finalize_date)
		return format_html(s)
	show_finalize_button.allow_tags = True
	show_finalize_button.short_description = 'Click to finalize mission'

class Report(models.Model):
	text = models.CharField(max_length = 10000)
	pub_date = models.DateField()
	related_mission = models.ForeignKey(Mission)
	related_char = models.ForeignKey(Char)

class NeuroRequest(models.Model):
	STATUS = (
		(0, 'Open'),
		(1, 'Closed'),
	)
	teacher = models.ForeignKey(Char, related_name = "%(app_label)s_%(class)s_teacher")
	pupil = models.ForeignKey(Char, related_name = "%(app_label)s_%(class)s_pupil")
	target_class = models.ForeignKey(Class)
	pub_date = models.DateField()
	status = models.PositiveIntegerField(choices = STATUS, default = 0)
	closed_date = models.DateField()

class BlogEntry(CommonToken):
	author = models.ForeignKey(Account)
	text = models.CharField(max_length=10000)
	pub_date = models.DateField()

