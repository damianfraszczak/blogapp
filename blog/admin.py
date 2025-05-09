from django.contrib import admin

# Register your models here.
from .models import Post


@admin.register(Post)
class PostModel(admin.ModelAdmin):
    list_display = (
        "title",
        "slug",
        "author",
        "publish",
        "status",
    )
    search_fields = (
        "title",
        "body",
    )
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")
