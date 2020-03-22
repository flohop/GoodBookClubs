from django.contrib import admin
from .models import Book, Profile, DiscussionGroup, ReadingGroup,  Genre


class AdminClass(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Profile, AdminClass)
admin.site.register(Book, AdminClass)
admin.site.register(DiscussionGroup, AdminClass)
admin.site.register(ReadingGroup, AdminClass)
admin.site.register(Genre, AdminClass)