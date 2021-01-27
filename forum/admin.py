from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Post, Category, Thread


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("colored_name", "slug", "url")


admin.site.register(Post, MPTTModelAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register([Thread])
