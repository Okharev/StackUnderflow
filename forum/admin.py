from django.contrib import admin

from .models import Post, Category, Thread, Karma

"""class CategoryAdmin(admin.ModelAdmin):
    list_display = ("colored_name", "slug", "url")


admin.site.register(Category, CategoryAdmin)
"""
admin.site.register([Thread, Karma, Post, Category])
