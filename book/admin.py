from django.contrib import admin
from .models import Book, Genre

# Register your models here.


class AdminClass(admin.ModelAdmin):
    readonly_fields = ('id',)


admin.site.register(Book, AdminClass)
admin.site.register(Genre, AdminClass)
