from django.contrib import admin
from issues.models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Skill)
