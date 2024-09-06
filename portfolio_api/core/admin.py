from django.contrib import admin

from . import models

admin.site.register(models.UserLimits)
admin.site.register(models.AllowedImageMimeType)
