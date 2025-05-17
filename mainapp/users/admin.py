from django.contrib import admin, messages
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email', 'phone', 'date_joined')
    list_display_links = ('id', 'username', 'first_name')
    ordering = ['-id', 'date_joined', 'username', 'first_name', 'last_name', 'email', 'phone']
    search_fields = ['id', 'first_name__icontains', 'username__icontains', 'last_name__icontains', 'email__icontains',
                     'phone', 'groups__name__icontains']
    list_filter = ['id', 'username', 'first_name', 'last_name', 'email', 'phone', 'groups']
    list_per_page = 100
