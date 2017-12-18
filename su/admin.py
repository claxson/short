from django.contrib import admin

import models

# Register your models here.
@admin.register(models.Var)
class VarAdmin(admin.ModelAdmin):
    list_display = ['id', 'key', 'value' ]

@admin.register(models.Url)
class UrlAdmin(admin.ModelAdmin):
    list_display = ['id','short' ,'real' ]


