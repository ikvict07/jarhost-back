from django.contrib import admin
from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    fields = ('username',
              'first_name',
              'last_name',
              'isFundraiser',
              'email',
              'monoid',
              'about',
              'last_login',
              'is_superuser',
              'groups',
              'user_permissions',
              'is_staff',
              'is_active',
              'date_joined',
              )


admin.site.register(CustomUser, CustomUserAdmin)
