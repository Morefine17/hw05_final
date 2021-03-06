from django.contrib import admin

from .models import Group, Post

EMPTY = "-пусто-"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("author", "text", "pub_date", "pk", "group")
    list_editable = ("group",)
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = EMPTY


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = ("title", "description")
    search_fields = ("description",)
    list_filter = ("title",)
    empty_value_display = EMPTY
