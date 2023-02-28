from django.contrib import admin

# Register your models here.
from .models import Projects,Tags,Review

admin.site.register(Projects)
admin.site.register(Tags)
admin.site.register(Review)