from django.contrib import admin
from .models import Profile


class AdminClass(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Profile, AdminClass)