from django.contrib import admin
from .models import VersionUpdate

@admin.register(VersionUpdate)
class VersionUpdateAdmin(admin.ModelAdmin):
    list_display = ('user', 'version', 'created_at')
    search_fields = ('user__username', 'version', 'summary', 'highlights')
    list_filter = ('user', 'created_at')
