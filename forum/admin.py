from django.contrib import admin
from . import models
from mptt.admin import MPTTModelAdmin


@admin.register(models.Question)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'slug', 'author')
    prepopulated_fields = {'slug': ('title',), }



admin.site.register(models.Answer, MPTTModelAdmin)


