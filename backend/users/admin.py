from django.contrib import admin

from .mixins import DisplayEmptyFieldMixin
from .models import Subscription, User


@admin.register(User)
class UserAdmin(DisplayEmptyFieldMixin, admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('username', 'email')


@admin.register(Subscription)
class SubscriptionAdmin(DisplayEmptyFieldMixin, admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user', 'author')
    list_filter = ('user', 'author')
