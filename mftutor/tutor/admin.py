# vim: set fileencoding=utf8 :
from .models import *
from django.contrib import admin

class TutorInline(admin.TabularInline):
    model = Tutor

class TutorAdmin(admin.ModelAdmin):
    list_display = ('year', 'profile', 'is_tutorbest')
    list_display_links = ('profile',)
    list_filter = ('year',)
    search_fields = ['profile__user__first_name', 'profile__user__last_name']
    filter_horizontal = ('groups',)

def get_full_name(tutor):
    return tutor.get_full_name()
get_full_name.short_description = 'Navn'

class ProfileAdmin(admin.ModelAdmin):
    list_display = (get_full_name, 'studentnumber')
    inlines = [
            TutorInline,
    ]
    radio_fields = {'gender': admin.HORIZONTAL}
    search_fields = ['user__first_name', 'user__last_name']

def make_visible(modeladmin, request, queryset):
    queryset.update(visible=True)
make_visible.short_description = 'Gør synlig'

def make_invisible(modeladmin, request, queryset):
    queryset.update(visible=False)
make_invisible.short_description = 'Gør ikke synlig'

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'handle', 'visible')
    list_filter = ('visible',)
    search_fields = ['name', 'handle']
    actions = [make_visible, make_invisible]

class LeaderAdmin(admin.ModelAdmin):
    list_select_related = True
    list_display = ('year', 'group', 'tutor')
    list_display_links = ('tutor',)

def board_full_name(bm):
    return bm.tutor.profile.user.get_full_name()
board_full_name.short_description = 'Navn'

def tutor_year(bm):
    return bm.tutor.year
tutor_year.short_description = 'År'
tutor_year.admin_order_field = 'tutor__year'

class BoardAdmin(admin.ModelAdmin):
    list_display = (board_full_name, tutor_year, 'title', 'position')
    list_filter = ('tutor__year',)
    search_fields = ['tutor__profile__user__first_name', 'tutor__profile__user__last_name', 'title']
    list_editable = ('title', 'position',)

class RusClassAdmin(admin.ModelAdmin):
    list_display = ('year', 'internal_name', 'official_name', 'handle')
    list_display_links = ('internal_name',)
    search_fields = ['internal_name', 'official_name', 'handle']

class RusAdmin(admin.ModelAdmin):
    list_display = ('profile', 'year', 'rusclass')
    search_fields = ['profile__user__first_name', 'profile__user__last_name']

admin.site.register(Tutor, TutorAdmin)
admin.site.register(TutorProfile, ProfileAdmin)
admin.site.register(TutorGroup, GroupAdmin)
admin.site.register(TutorGroupLeader, LeaderAdmin)
admin.site.register(BoardMember, BoardAdmin)
admin.site.register(RusClass, RusClassAdmin)
admin.site.register(Rus, RusAdmin)
