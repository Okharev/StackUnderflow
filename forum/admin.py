from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("colored_name", "slug", "url")


admin.site.register(Post, MPTTModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register([Thread])
