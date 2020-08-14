from django.contrib import admin
from django.utils.html import format_html

from .models import CategoryList, ImgDetails, UserProfile


# Register your models here.


class ImgDetailsAdmin(admin.ModelAdmin):

    search_fields = ('Category','User','Valid','UploadDate')
    list_per_page = 25



admin.site.register(CategoryList)
admin.site.register(ImgDetails, ImgDetailsAdmin)
admin.site.register(UserProfile)
