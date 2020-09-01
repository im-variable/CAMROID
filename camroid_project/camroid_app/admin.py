from django.contrib import admin
from django.utils.html import format_html

from .models import CategoryList, ImgDetails, UserProfile


# Register your models here.

def MarkasValid (modeladmin, request, queryset):
    queryset.update(Valid = True)
MarkasValid.short_description = "Mark as Valid"

class ImgDetailsAdmin(admin.ModelAdmin):
    list_display = ['Img','Category', 'keywords', 'Valid', 'UploadDate']
    fields = ('Img', 'Category', 'keywords', 'Valid', 'UploadDate' )
    ordering = ['UploadDate']
    list_per_page = 25
    actions = [MarkasValid]


admin.site.register(CategoryList)
admin.site.register(ImgDetails, ImgDetailsAdmin)
admin.site.register(UserProfile)
