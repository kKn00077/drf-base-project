from django.contrib import admin
from .models import File, FileGroup


admin.site.register(FileGroup)
admin.site.register(File)
