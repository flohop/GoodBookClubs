from django.contrib import admin
from .models import DiscussionGroup, ReadingGroup, DiscussionComment, ReadingComment


class AdminClass(admin.ModelAdmin):
    readonly_fields = ('id',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'body', 'club', 'created_on', 'disabled')
    list_filter = ('disabled', 'created_on')
    readonly_fields = ('id',)
    search_fields = ('name', 'body')
    actions = ['disable_comments']

    def disable_comments(self, request, queryset):
        queryset.update(disabled=True)


admin.site.register(ReadingComment, CommentAdmin)
admin.site.register(DiscussionComment, CommentAdmin)
admin.site.register(DiscussionGroup, AdminClass)
admin.site.register(ReadingGroup, AdminClass)
