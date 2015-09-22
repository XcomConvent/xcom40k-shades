from django.contrib import admin

# Register your models here.

from .models import *

class CharAdmin(admin.ModelAdmin):
	list_display = ('name',)

class AbilityAdmin(admin.ModelAdmin):
	list_display = ('name', 'cls', 'required_level')

class MissionAdmin(admin.ModelAdmin):
	list_display = ('name', 'pub_date')

class ReportAdmin(admin.ModelAdmin):
	list_display = ('related_mission', 'related_char', 'pub_date')

class AccountAdmin(admin.ModelAdmin):
	list_display = ('user',)

class NeuroRequestAdmin(admin.ModelAdmin):
	list_display = ('pub_date', 'status', 'teacher', 'pupil')

class ClassLevelPairAdmin(admin.ModelAdmin):
	list_display = ('cls', 'level')

admin.site.register(Char, CharAdmin)
admin.site.register(Ability, AbilityAdmin)
admin.site.register(Class)
admin.site.register(Item)
admin.site.register(ItemToken)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(NeuroRequest, NeuroRequestAdmin)
admin.site.register(ClassLevelPair, ClassLevelPairAdmin)
