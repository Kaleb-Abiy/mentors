from django.contrib import admin
from .models import CustomeUser, Profile
from django.contrib.auth.admin import UserAdmin

# Register your models here.


class CustomeUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password", "is_user", "is_mentor")}),
        ("Permissions", {"fields": ("is_staff",
         "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "is_user", "is_mentor"
            )}
         ),
    )

    ordering = ('email',)


admin.site.register(CustomeUser, CustomeUserAdmin)
admin.site.register(Profile)
