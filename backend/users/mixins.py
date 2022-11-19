from django.contrib import admin


class DisplayEmptyFieldMixin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
