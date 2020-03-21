from django.contrib import admin
from .models import Book, Profile, DiscussionGroup, ReadingGroup,  Genre


admin.site.register(Profile)
admin.site.register(Book)
admin.site.register(DiscussionGroup)
admin.site.register(ReadingGroup)
admin.site.register(Genre)
