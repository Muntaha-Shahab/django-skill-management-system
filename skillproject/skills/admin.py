from django.contrib import admin
from .models import Skill

class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'user', 'proficiency_level', 'years_of_experience')
    list_filter = ('proficiency_level', 'user')
    search_fields = ('skill_name', 'user__username')

admin.site.register(Skill, SkillAdmin)
