from django.contrib import admin

from . import models


admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)
admin.site.register(models.Lyrics)
admin.site.register(models.LyricsCollection)