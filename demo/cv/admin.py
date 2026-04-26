from django.contrib import admin
from .models import CVProfile, Experience, Education, Skill, Language

admin.site.register(CVProfile)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Skill)
admin.site.register(Language)
