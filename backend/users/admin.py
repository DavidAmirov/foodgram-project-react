from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    list_display_links = ('email',)
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
