from django.contrib import admin

# Register your models here.

from .models import *

def finalize_mission(modeladmin, request, queryset):
	for mis in queryset:
		mis.status = 3
		mis.save()
finalize_mission.short_description = "Finalize selected missions"

class CharAdmin(admin.ModelAdmin):
	list_display = ('name','class_level_pairs')
	view_on_site = True

class AbilityAdmin(admin.ModelAdmin):
#	list_display_links = ('name', 'cls',)
	list_display = ('name', 'cls', 'required_level')

class MissionAdmin(admin.ModelAdmin):
	list_display = ('name', 'status', 'pub_date', 'show_finalize_button')
	actions = [finalize_mission]

class ReportAdmin(admin.ModelAdmin):
	list_display = ('related_mission', 'related_char', 'pub_date')
	#fields = (('related_mission', 'related_char'), 'pub_date')
	fieldsets = (
		(None, {'fields':(('related_char', 'related_mission',),)}),	
		('Report', {'fields':('text', 'pub_date',), 'classes': 'extrapretty'}),
	)

class AccountAdmin(admin.ModelAdmin):
	list_display = ('user',)

class NeuroRequestAdmin(admin.ModelAdmin):
	list_display = ('pub_date', 'status', 'teacher', 'pupil')
	list_filter = ('status', 'pub_date')

class ClassLevelPairAdmin(admin.ModelAdmin):
	list_display = ('cls', 'level')

class ItemTokenInline(admin.TabularInline):
	model = ItemToken

class ItemAdmin(admin.ModelAdmin):
	inlines = [ItemTokenInline,]

class ItemTokenAdmin(admin.ModelAdmin):
	pass

class BlogEntryAdmin(admin.ModelAdmin):
#	formfield_overrides = {
#		models.TextField: {'widget': RichTextEditorWidget},
#	}
	list_display = ('author', 'pub_date',)
	fieldsets = (
		(None, {'fields': (('author', 'pub_date',),)}),
		('Post', {'fields': (('text',),)}),
	)

admin.site.register(BlogEntry, BlogEntryAdmin)
admin.site.register(Char, CharAdmin)
admin.site.register(Ability, AbilityAdmin)
admin.site.register(Class)
admin.site.register(Item, ItemAdmin)
admin.site.register(ItemToken, ItemTokenAdmin)
admin.site.register(Mission, MissionAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(NeuroRequest, NeuroRequestAdmin)
admin.site.register(ClassLevelPair, ClassLevelPairAdmin)
admin.site.register(ItemMarketToken)