from django.contrib import admin
from .models import Items


class ItemsAdmin(admin.ModelAdmin):

    list_display = ['id', 'name', 'category', 'comment']  # Add filter on top of table
    search_fields = ['name', 'comment']             # Add a search bar that searches according to the parameters

admin.site.register(Items, ItemsAdmin)  # Add a model in admin
