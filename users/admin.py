from django.contrib import admin
from django.utils.html import format_html
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'profession', 'profile_picture_display', 'is_active', 'is_staff')

    def profile_picture_display(self, obj):
        return format_html('<img src="{}" style="height: 80px; width: 80px; border-radius: 50%;" />'.format(obj.profile_picture.url))

    profile_picture_display.short_description = 'Profile Picture'


    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'email', 'first_name', 'last_name', 'is_active', 'is_staff')
        }),
        ('Additional Information', {
            'fields': ('profile_picture', 'profession'),
        }),
    )



