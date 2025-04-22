from django.contrib import admin

from users.models import BlogUser, Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "site")
    search_fields = ("name",)
    list_filter = ("site",)


@admin.register(BlogUser)
class BlogUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "company")
    search_fields = ("username", "email", "first_name", "last_name")
    list_filter = ("company",)
